# agent.py
from config import client
import json

def get_response(user_input: str, temperature=0.9, top_p=0.8):
    """
    Fetch marketing ideas from Groq with streaming.
    Returns JSON-formatted output.
    """
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": """Act as a creative marketing assistant. 
                    Return ALL responses strictly as valid JSON.
                    Structure the JSON as follows:
                    {
                      "campaign_title": "string",
                      "summary": "string",
                      "target_audience": ["list", "of", "segments"],
                      "channels": ["list", "of", "recommended", "channels"],
                      "creative_ideas": ["list", "of", "concepts"],
                      "estimated_budget": "string or numeric",
                      "kpis": ["list", "of", "key performance indicators"]
                    }
                    Ensure no extra commentary or text outside the JSON.
                    """
                },
                {"role": "user", "content": user_input}
            ],
            temperature=temperature,
            max_completion_tokens=4096,
            top_p=top_p,
            stream=False,  # easier for parsing JSON
        )

        # Extract content
        response = completion.choices[0].message.content.strip()

        # Try to parse JSON
        try:
            data = json.loads(response)
            return json.dumps(data, indent=2)
        except json.JSONDecodeError:
            # In case the model added extra text, attempt to recover JSON
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end != -1:
                cleaned = response[start:end]
                data = json.loads(cleaned)
                return json.dumps(data, indent=2)
            else:
                return json.dumps({"error": "Invalid JSON format", "raw_response": response}, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)