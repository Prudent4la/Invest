"""
Optional Day 3 Stretch Exercise - Batch Lead Analyzer

Reads data/sample_leads.csv and writes output/analyzed_leads.csv.
This is intentionally a stretch activity; the core 09:00-14:00 class
can finish after 03_lead_analyzer.py.
"""

import csv
import json
import os
import time
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

PROJECT_ENDPOINT = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
MODEL_NAME = os.getenv("FOUNDRY_MODEL_NAME")

INPUT_FILE = Path("data/sample_leads.csv")
OUTPUT_FILE = Path("output/analyzed_leads.csv")

INSTRUCTIONS = """
Classify the customer enquiry.

Return ONLY valid JSON:
{
  "intent": "purchase|support|information|other",
  "urgency": "low|medium|high",
  "lead_score": 0,
  "summary": "short summary",
  "recommended_action": "short action"
}

lead_score must be an integer from 0 to 100.
Do not invent information.
Return JSON only.
"""


def create_client():
    project = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential(),
    )
    return project.get_openai_client()


def analyze(client, enquiry):
    response = client.responses.create(
        model=MODEL_NAME,
        input=f"{INSTRUCTIONS}\n\nCUSTOMER ENQUIRY:\n{enquiry}",
    )
    return json.loads(response.output_text)


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    client = create_client()

    with INPUT_FILE.open("r", encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source))

    output_rows = []

    for row in rows:
        enquiry = row["enquiry"]

        print(f"Analyzing lead {row['lead_id']}...")

        try:
            result = analyze(client, enquiry)
            output_rows.append(
                {
                    **row,
                    "intent": result.get("intent", ""),
                    "urgency": result.get("urgency", ""),
                    "lead_score": result.get("lead_score", ""),
                    "summary": result.get("summary", ""),
                    "recommended_action": result.get(
                        "recommended_action", ""
                    ),
                    "status": "success",
                    "error": "",
                }
            )
        except Exception as exc:
            output_rows.append(
                {
                    **row,
                    "intent": "",
                    "urgency": "",
                    "lead_score": "",
                    "summary": "",
                    "recommended_action": "",
                    "status": "error",
                    "error": str(exc),
                }
            )

        # Simple classroom pacing to avoid sending all requests at once.
        time.sleep(1)

    fieldnames = [
        "lead_id",
        "customer_name",
        "company",
        "enquiry",
        "intent",
        "urgency",
        "lead_score",
        "summary",
        "recommended_action",
        "status",
        "error",
    ]

    with OUTPUT_FILE.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"\nFinished. Results written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
