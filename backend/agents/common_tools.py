import json
import re

from langchain_core.messages import AIMessage


def extract_json_from_ai_message(ai_msg: AIMessage = None) -> dict:
    content = ai_msg.content

    clean = re.sub(r"^```json|^```|```$", "", content.strip(), flags=re.MULTILINE).strip()

    data = json.loads(clean)

    return data
