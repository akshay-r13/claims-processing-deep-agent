import ast
import operator
from pathlib import Path
from config.paths import DATA_DIR
import pdfplumber
from langchain_core.tools import tool


@tool
def read_pdf(path: str) -> str:
    """Extract the text of one PDF under /data
    e.g. /data/claims/CLM-1004/receipts/meal_2026-10-14_dinner.pdf. Returns plain text."""
    try:
        full = resolve_data_path(path)
    except ValueError as e:
        return f"ERROR: {e}"
    if not full.is_file() or full.suffix.lower() != ".pdf":
        return f"ERROR: not a PDF file: {path}"
    with pdfplumber.open(full) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    return text.strip() or "ERROR: no extractable text (scanned image? needs OCR or a vision model)"


@tool
def calculate(expression: str) -> str:
    """Evaluate a python arithmetic expression.
    Supports + - * / parentheses and min(), max(), round().
    Use it for EVERY sum, percentage, cap and comparison; never do arithmetic yourself.
    Example: min(302.40, 6 * 50)"""
    try:
        result = eval(ast.parse(expression, mode="eval").body)
    except Exception as e:
        return f"ERROR: {e}"
    return f"{round(result, 2):.2f}"


def resolve_data_path(virtual_path: str) -> Path:
    """Map agent path under /data/ to real file.
    Reject anything that escapes the data directory."""
    rel = virtual_path.removeprefix("/data").lstrip("/")
    full = (DATA_DIR / rel).resolve()
    root = DATA_DIR.resolve()
    if full != root and root not in full.parents:
        raise ValueError(f"Path outside data directory: {virtual_path}")
    return full

def eval(node):
    SUPPORTED_OPERATIONS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
    SUPPORTED_FUNCTIONS = {"min": min, "max": max, "round": round}
    # Plain numeric value, base condition
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    # + , - , x and / operations
    if isinstance(node, ast.BinOp) and type(node.op) in SUPPORTED_OPERATIONS:
        return SUPPORTED_OPERATIONS[type(node.op)](eval(node.left), eval(node.right))
    # negative inversion
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -eval(node.operand)
    # functions min max and round
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id in SUPPORTED_FUNCTIONS and not node.keywords):
        return SUPPORTED_FUNCTIONS[node.func.id](*[eval(a) for a in node.args])
    raise ValueError("unsupported expression")