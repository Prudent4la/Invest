"""
Day 3 - Lab 2A: Test Microsoft Foundry Connection

This is the smallest useful model call in the project.
Run this before attempting the Lead Analyzer.
"""

import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
model_name = os.getenv("FOUNDRY_MODEL_NAME")

if not endpoint:
    raise ValueError(
        "FOUNDRY_PROJECT_ENDPOINT is missing. "
        "Create a .env file from .env.example and add the project endpoint."
    )

if not model_name:
    raise ValueError(
        "FOUNDRY_MODEL_NAME is missing. "
        "Add the model/deployment name to your .env file."
    )

print("Creating Microsoft Foundry project client...")

project = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

openai_client = project.get_openai_client()

print("Sending a test request to the model...")

response = openai_client.responses.create(
    model=model_name,
    input="Explain Microsoft Azure in one sentence.",
)

if not response.output_text or not response.output_text.strip():
    raise RuntimeError("The model returned an empty text response.")

print("\nMODEL RESPONSE")
print("-" * 60)
print(response.output_text)
print("-" * 60)
print("SUCCESS: Python communicated with the model.")
