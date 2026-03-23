from backend.services.ai_service import get_ai_response
import sys
import os

sys.path.append(os.path.abspath("."))
prompt = "Explain in one sentence why recent and reliable records are usually more trustworthy."
result = get_ai_response(prompt)

print(result)