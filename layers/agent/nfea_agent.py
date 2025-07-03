import os
from google import genai
from core.secrets import get_secret_value

class NFEAAgent:
    def __init__(self):
        self.api_key = get_secret_value("GoogleAPIStudio")
        self.client = genai.Client(api_key=self.api_key)
        prompt_path = os.path.join("system_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    def process(self, user_input):
        from google.genai import types
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                response_mime_type='application/json',
            ),
        )
        return response.text
