🚀 Serverless AI Blog Generator with Safety Guardrails

A full-stack serverless application that uses Amazon Bedrock (Nova Micro) to generate high-quality blog posts. This project implements enterprise-grade Responsible AI practices using Amazon Bedrock Guardrails to filter harmful content and protect PII (Personally Identifiable Information).<img width="1756" height="903" alt="Screenshot 2025-11-28 132538" src="https://github.com/user-attachments/assets/87d0a129-0428-48d6-94ff-cf731509fb17" />





🏗️ Architecture<img width="1120" height="619" alt="Screenshot 2025-11-28 133100" src="https://github.com/user-attachments/assets/49779727-52cf-4d8f-88b8-b559a2d39251" />


This project demonstrates a fully serverless "Generative AI as a Service" pattern with a dedicated safety layer:

Frontend (S3) → API Gateway → Lambda → [Guardrails Check] → Amazon Bedrock (Nova Micro)

Frontend: A responsive HTML/JS/Tailwind web app hosted on Amazon S3 (Static Website Hosting) with CloudFront distribution logic.

API Layer: Amazon API Gateway (HTTP API) manages requests, handles CORS, and routes traffic.

Backend: AWS Lambda (Python 3.12) processes input and orchestrates the AI interaction.

Safety Layer: Amazon Bedrock Guardrails intercepts prompts to filter hate speech, violence, and PII before they reach the model.

AI Model: Amazon Nova Micro generates the content using cross-region inference for high availability and low cost.

🛠️ Tech Stack

Cloud Provider: AWS

AI Model: Amazon Nova Micro (Serverless Inference)

AI Safety: Amazon Bedrock Guardrails

Compute: AWS Lambda (Python Boto3)

Storage/Hosting: Amazon S3

API: Amazon API Gateway

Frontend: HTML5, Tailwind CSS, JavaScript (Fetch API)

🛡️ AI Safety & Guardrails Implementation

To ensure the application is safe for public use, I implemented a robust Guardrail system:

Content Filters: High-strength filters for Hate, Insults, Sexual, and Violence.

Denied Topics: Blocks generation of political content or controversial subjects.

PII Protection: Automatically blocks inputs containing Email Addresses or Phone Numbers to prevent data leakage.

Custom Messaging: Returns a polite refusal message ("I cannot generate content on this topic...") instead of crashing or generating harmful text.

🚀 How It Works

User enters a Topic and selects a Tone.

The browser sends a POST request to the API Gateway endpoint.

Lambda receives the request and constructs a structured prompt.

The Guardrail Check: Before generating text, AWS Bedrock scans the prompt against the defined rules.

If Unsafe: The request is blocked immediately, and a canned safety message is returned.

If Safe: The prompt is passed to the Nova Micro model.

The result is displayed instantly on the frontend with modern glassmorphism UI effects.


🔧 Setup & Deployment

This project was built using AWS Managed Services via the Console (ClickOps):

Guardrails: Configured content filters and PII blocking in the Bedrock Console.

Lambda: Created a Python function with AmazonBedrockFullAccess IAM permissions and increased timeout to 30s.

API Gateway: Configured an HTTP API with strict CORS enabled (Access-Control-Allow-Origin restricted to S3).

S3: Enabled Static Website Hosting and configured a Bucket Policy for public read access.

Cost Optimization: Reduced max_new_tokens to 300 to limit generation costs.

💰 Cost Analysis

This architecture is designed for extreme cost efficiency, even with Guardrails active:

Hosting: S3 Static hosting costs pennies per month.

Compute: Lambda allows 400,000 GB-seconds free.

AI: Nova Micro is priced at ~$0.035 per 1M input tokens.

Guardrails: ~$0.15 per 1M characters scanned.

Total Estimated Cost: < $0.50/month for personal portfolio usage.
