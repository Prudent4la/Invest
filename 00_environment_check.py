"""
Day 3 - Environment Check

Purpose:
- Confirm Python can read the .env file.
- Confirm the required environment variables exist.
- This script does NOT call Microsoft Foundry.
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
model_name = os.getenv("FOUNDRY_MODEL_NAME")

print("=" * 60)
print("DAY 3 ENVIRONMENT CHECK")
print("=" * 60)
print(f"Python version: {sys.version.split()[0]}")
print(f"Project endpoint configured: {'YES' if endpoint else 'NO'}")
print(f"Model/deployment configured: {'YES' if model_name else 'NO'}")

if not endpoint:
    print("\nACTION: Add FOUNDRY_PROJECT_ENDPOINT to your .env file.")

if not model_name:
    print("ACTION: Add FOUNDRY_MODEL_NAME to your .env file.")

if endpoint and model_name:
    print("\nEnvironment configuration looks ready.")
else:
    raise SystemExit("\nEnvironment configuration is incomplete.")
