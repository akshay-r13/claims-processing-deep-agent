from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "outputs"
CLAIM_REQUESTS_DIR = DATA_DIR / "claim_requests"
CLAIM_REQUESTS_LIST = CLAIM_REQUESTS_DIR / "claim_requests.csv"
CLAIM_SUPPORTING_DOCS_DIR = CLAIM_REQUESTS_DIR / "submitted_documents"