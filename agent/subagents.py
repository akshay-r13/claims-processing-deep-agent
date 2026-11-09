from .tools import calculate, read_pdf

RECEIPT_READER = {
    "name": "receipt-reader",
    "description": (
        "Reads ONE receipt PDF and saves its extracted fields as JSON. "
        "Give it the receipt path and the output path. "
        "It returns a one-line summary, not the receipt text."
    ),
    "system_prompt": """You extract data from one receipt PDF.
        1. Call read_pdf on the path you are given.
        2. Build a JSON object with: file, vendor, receipt_no, date, line_items
        (list of {description, amount}), subtotal, tax, tip, total,
        payment_method, notes. Put anything unusual in notes (mismatched totals,
        'copy' markers, missing fields). Use null for absent fields. Do not invent values.
        3. Use calculate to check that line items, tax and tip add up to the total.
        Record any mismatch in notes.
        4. Save the JSON with write_file to the output path you were given.
        5. Reply with ONE line: vendor | date | total | output path.
        Never return the raw receipt text.""",
    "tools": [read_pdf, calculate],
}