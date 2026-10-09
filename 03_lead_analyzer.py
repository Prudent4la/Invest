"""
Day 3 - Lab 3: AI Lead Analyzer

Flow:
1. Read a customer enquiry.
2. Send clear business instructions + the enquiry to the model.
3. Ask the model for JSON.
4. Parse the JSON.
5. Validate required fields and lead_score.
6. Display the business-ready result.
"""

import json
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

PROJECT_ENDPOINT = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
MODEL_NAME = os.getenv("FOUNDRY_MODEL_NAME")

if not PROJECT_ENDPOINT:
    raise ValueError("FOUNDRY_PROJECT_ENDPOINT is missing from .env.")

if not MODEL_NAME:
    raise ValueError("FOUNDRY_MODEL_NAME is missing from .env.")

SYSTEM_INSTRUCTIONS = """
You are an AI business enquiry classifier.

Analyse the customer enquiry.

Return ONLY valid JSON using this exact structure:

{
  "intent": "purchase|support|information|other",
  "urgency": "low|medium|high",
  "lead_score": 0,
  "summary": "short summary",
  "recommended_action": "short action",
  "requires_human_review": false
}

Rules:
1. lead_score must be an integer between 0 and 100.
2. requires_human_review must be a boolean: true if the lead is complex, angry, suspicious, or requires manual human intervention; otherwise false.
3. Do not invent customer information.
4. Strong purchase intent and an urgent timeline can justify a higher lead score.
5. Support requests should not be treated as sales leads.
6. If the enquiry is unclear, use "other" or "information" as appropriate.
7. Return JSON only. Do not wrap it in Markdown code fences.
"""


def create_client():
    """Create an authenticated model client for the Foundry project."""
    project = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential(),
    )
    return project.get_openai_client()


def analyse_lead(client, enquiry):
    """Send the business instructions and customer enquiry to the model."""
    prompt = f"""
{SYSTEM_INSTRUCTIONS}

CUSTOMER ENQUIRY:
{enquiry}
"""

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )

    if not response.output_text or not response.output_text.strip():
        raise RuntimeError("The model returned an empty response.")

    return response.output_text.strip()


def validate_response(raw_response):
    """Parse and validate the model's JSON before business logic uses it."""
    try:
        result = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "The model did not return valid JSON. "
            "Review the raw response and the output instructions."
        ) from exc

    required_fields = {
        "intent",
        "urgency",
        "lead_score",
        "summary",
        "recommended_action",
        "requires_human_review",
    }

    missing_fields = required_fields - result.keys()

    if missing_fields:
        raise ValueError(
            f"Missing required field(s): {sorted(missing_fields)}"
        )

    allowed_intents = {"purchase", "support", "information", "other"}
    allowed_urgencies = {"low", "medium", "high"}

    if result["intent"] not in allowed_intents:
        raise ValueError(
            f"Invalid intent: {result['intent']}. "
            f"Allowed values: {sorted(allowed_intents)}"
        )

    if result["urgency"] not in allowed_urgencies:
        raise ValueError(
            f"Invalid urgency: {result['urgency']}. "
            f"Allowed values: {sorted(allowed_urgencies)}"
        )

    if not isinstance(result["requires_human_review"], bool):
        raise ValueError("requires_human_review must be a boolean.")

    score = result["lead_score"]

    if isinstance(score, bool) or not isinstance(score, int):
        raise ValueError("lead_score must be an integer.")

    if score < 0 or score > 100:
        raise ValueError("lead_score must be between 0 and 100.")

    return result


def main():
    print("=" * 60)
    print("AI LEAD ANALYZER")
    print("=" * 60)

    enquiry = input("\nEnter the customer enquiry:\n> ").strip()

    if not enquiry:
        print("\nERROR: The enquiry cannot be empty.")
        return

    client = create_client()

    try:
        raw_response = analyse_lead(client, enquiry)

        print("\nRAW MODEL RESPONSE")
        print("-" * 60)
        print(raw_response)

        result = validate_response(raw_response)

        print("\nVALIDATED RESULT")
        print("-" * 60)
        print(json.dumps(result, indent=4))

        if result["intent"] == "purchase" and result["lead_score"] >= 70:
            print("\nBUSINESS RULE")
            print("High-value sales lead -> prioritise sales follow-up.")
        elif result["intent"] == "support":
            print("\nBUSINESS RULE")
            print("Support request -> route to customer support.")
        else:
            print("\nBUSINESS RULE")
            print("Standard follow-up / review.")

    except Exception as error:
        print("\nERROR")
        print("-" * 60)
        print(str(error))


if __name__ == "__main__":
    main()
