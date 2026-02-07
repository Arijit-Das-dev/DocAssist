from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

class GroqModel:

    def __init__(
        self,
        model="llama-3.3-70b-versatile",
        prompt_path="prompt.txt"
    ):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = model
        self.system_prompt = self._load_prompt(prompt_path)

    def _load_prompt(self, path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(base_dir, path)

        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read().strip()


    def stream_chat(
        self,
        user_message,
        temperature=1,
        max_tokens=1024,
        top_p=1
    ):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=max_tokens,
            top_p=top_p,
            stream=True
        )

        for chunk in completion:
            yield chunk.choices[0].delta.content or ""