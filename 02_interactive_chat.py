"""
Day 3 - Lab 2B: Interactive Chat

Purpose:
- Replace a hard-coded prompt with user input.
- Demonstrate the request/response loop.
"""

import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
model_name = os.getenv("FOUNDRY_MODEL_NAME")

if not endpoint or not model_name:
    raise ValueError(
        "Missing Foundry configuration. Check FOUNDRY_PROJECT_ENDPOINT "
        "and FOUNDRY_MODEL_NAME in .env."
    )

project = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

openai_client = project.get_openai_client()

print("=" * 60)
print("INTERACTIVE MODEL TEST")
print("=" * 60)

user_input = input("\nAsk the model a question:\n> ").strip()

if not user_input:
    raise ValueError("The question cannot be empty.")

response = openai_client.responses.create(
    model=model_name,
    input=user_input,
)

print("\nMODEL RESPONSE")
print("-" * 60)
print(response.output_text)
