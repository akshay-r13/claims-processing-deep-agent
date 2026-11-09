"""Wrapper custom class for logging thoughts, and tool calls"""

from .agent import build_agent # core deep agent

class ClaimsAgent:
    
    def __init__(self):
        self.agent = build_agent()

    def process_claim(self, claim_data):
        prompt = (
            f"Review this expense claim."
            f"---"
            f"claim_id - {claim_data['claim_id']}"
            f"employee_id - {claim_data['employee_id']}"
            f"submitted_date - {claim_data['submitted_date']}"
            f"category - {claim_data['category']}"
            f"description - {claim_data['description']}"
            f"expense_dates - {claim_data['expense_dates']}"
            f"attendees - {claim_data['attendees']}"
            f"business_purpose - {claim_data['business_purpose']}"
            f"travel_request_id - {claim_data['travel_request_id']}"
            f"claimed_amount - {claim_data['claimed_amount']}"
            f"---"
        )
        inputs = {"messages": [{"role": "user", "content": prompt}]}
        
        self.agent.invoke(inputs, verbose=True)

claims_agent = ClaimsAgent()