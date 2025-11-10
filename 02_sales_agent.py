# sales_agent.py
from config import client
from tools import filter_products_tool, check_inventory_tool, checkout_tool
import json

def get_sales_response(user_input: str, temperature=0.7, top_p=0.8):
    """
    Sales assistant AI — suggests products and uses tools for inventory, checkout, etc.
    Returns structured JSON.
    """
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful e-commerce sales assistant.
                    You can recommend products, check inventory, and assist with checkout.
                    Always respond strictly in valid JSON like this:
                    {
                      "intent": "product_recommendation | check_inventory | checkout",
                      "user_query": "string",
                      "recommended_products": ["list of product names"],
                      "inventory_status": {"product_name": "in_stock | out_of_stock"},
                      "cart_update": {"added": ["items"], "removed": ["items"]},
                      "final_message": "string summary or confirmation"
                    }
                    No extra commentary outside JSON.
                    """
                },
                {"role": "user", "content": user_input}
            ],
            temperature=temperature,
            max_completion_tokens=2048,
            top_p=top_p,
            stream=False
        )

        response = completion.choices[0].message.content.strip()

        try:
            data = json.loads(response)
        except json.JSONDecodeError:
            start = response.find("{")
            end = response.rfind("}") + 1
            data = json.loads(response[start:end])

        # Tool logic based on intent
        intent = data.get("intent", "")
        if intent == "check_inventory":
            result = check_inventory_tool.run(data.get("recommended_products", []))
            data["inventory_status"] = result
        elif intent == "product_recommendation":
            result = filter_products_tool.run(data.get("user_query", ""))
            data["recommended_products"] = result
        elif intent == "checkout":
            result = checkout_tool.run(data.get("cart_update", {}).get("added", []))
            data["cart_update"]["final_status"] = result

        return json.dumps(data, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)