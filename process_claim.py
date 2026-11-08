import argparse
import csv
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from agent import claims_agent

DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).parent / "outputs"
CLAIM_REQUESTS_LIST = DATA_DIR / "claim_requests" / "claim_requests.csv"

parser = argparse.ArgumentParser(
    description=f"A script that processes a claim request from {CLAIM_REQUESTS_LIST}"
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
    claims_agent.process_claim(claim_data)