import httpx
from config import settings
from exceptions.external_service_exception import ChatGptAnalysisException


class ChatGptClient:
    async def generate_recommendations(self, prompt: str, language_code: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f'Bearer {settings.openai_api_key}',
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-5.4-mini",
                    "messages": [
                        {
                        "role": "system",
                        "content":
                            f"""
            You are a delivery assistant in a courier app.

            Task:
            Generate one concise route recommendation block for the courier based on risky or delayed deliveries. 
            Do not include On time orders. Only suggest actions to avoid or reduce delays. And return text of recommendation by this language code: {language_code}

            Rules:
            - Maximum 3 sentences
            - Be practical and actionable
            - Focus on which deliveries to prioritize or monitor
            - Use only the delivery address and position in the route to identify orders; do not use order IDs
            - Do not explain calculations or reasoning
            - Do not include motivational phrases
            - Courier makes the final decision
            """,
                        },
            {"role": "user", "content": prompt},
          ],
                },
            )
        if response.status_code != 200:
            raise ChatGptAnalysisException()
        
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()