import os

from openai import OpenAI

from app.core.config import settings


def generate_completion(prompt: str) -> str:
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=settings.llm_github_token or os.getenv("LLM_GITHUB_TOKEN"),
    )
    response = client.responses.create(
        model="gpt-4o",
        input=prompt,
    )
    return response.output_text.strip()
