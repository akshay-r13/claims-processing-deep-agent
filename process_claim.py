import argparse
import csv

from dotenv import load_dotenv
load_dotenv()

from agent import claims_agent
from config.paths import DATA_DIR, CLAIM_REQUESTS_LIST


parser = argparse.ArgumentParser(
    description=(
        f"A Script that processes a claim request from {CLAIM_REQUESTS_LIST}"
        "Example: process_claim.py CLM-1001"
        f"The script spawns an agent which processes the request by investigating supporting documents and previous claim history from {DATA_DIR}"
    )
)
parser.add_argument("claim_id", type=str, help=f"ID of Claim from file {CLAIM_REQUESTS_LIST}")


def load_claim(claim_id):
    with open(CLAIM_REQUESTS_LIST, newline="") as f:
        for row in csv.DictReader(f):
            if row["claim_id"] == claim_id:
                return row
    raise Exception(f"Unknown claim: {claim_id}, not found in {CLAIM_REQUESTS_LIST}")


if __name__ == "__main__":
    args = parser.parse_args()
    claim_data = load_claim(args.claim_id)
    claims_agent.process_claim(claim_data, log_tool_calls=True, log_thoughts=True)