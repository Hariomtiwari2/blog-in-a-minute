import json
import boto3
import os

# Initialize the Bedrock client
# We explicitly set region_name='us-east-1' because Nova Micro is US-based.
bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    """
    Architecture Flow:
    1. User (Frontend) -> API Gateway -> This Lambda
    2. This Lambda -> Guardrail Check
    3. If Safe -> Amazon Bedrock (Nova Micro) -> Returns Blog
    4. If Unsafe -> Returns "Blocked Message" immediately
    """
    
    # 1. Parse Input
    try:
        body = json.loads(event.get('body', '{}'))
        topic = body.get('topic', 'Cloud Computing')
        tone = body.get('tone', 'Professional')
    except:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid input'})
        }

    # 2. System Prompt
    system_prompt = [{"text": "You are an expert technical content writer. Output HTML formatted content directly without markdown code blocks."}]

    # 3. User Prompt
    user_message = f"""
    Write a short blog post about: "{topic}".
    Tone: {tone}
    Format: Use HTML tags (<h1>, <h2>, <p>, <ul>, <li>) for structure. Do not include <html> or <body> tags.
    Length: Short and concise, approximately 100 words.
    Include a catchy title in an <h1> tag.
    """

    # 4. Construct Payload
    payload = {
        "inferenceConfig": {
            # COST CONTROL: Reduced to 300 tokens (approx 200 words max) to prevent overspending
            "max_new_tokens": 300,
            "temperature": 0.7
        },
        "system": system_prompt,
        "messages": [
            {
                "role": "user",
                "content": [{"text": user_message}]
            }
        ]
    }

    try:
        # 5. Call Bedrock WITH GUARDRAILS
        response = bedrock.invoke_model(
            modelId="us.amazon.nova-micro-v1:0",
            body=json.dumps(payload),
            
            # --- GUARDRAIL CONNECTION ---
            # Updated with your new US Region Guardrail ID
            guardrailIdentifier="vja0e60euysw", 
            guardrailVersion="DRAFT",
        )
        
        # 6. Parse Response
        response_body = json.loads(response['body'].read())
        
        # Nova Micro returns the result in this path.
        # If blocked, 'text' will contain your "I'm sorry..." message.
        blog_content = response_body['output']['message']['content'][0]['text']
        
        # 7. Return to Frontend
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'blog_post': blog_content})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'error': str(e)})
        }
