from langchain_openai import OpenAI
from config import LLM_BASE_URL, LLM_API_KEY, LLM_TEMPERATURE

class LLMService:
    """A wrapper for the LLM to keep all Langchain logic in one place"""
    def __init__(self):
        try:
            self.llm = OpenAI(
                base_url=LLM_BASE_URL,
                api_key=LLM_API_KEY,
                temperature=LLM_TEMPERATURE
            )
            print("[Log]: LLM Service initialized successfully")
        except Exception as e:
            print(f"[Error]: Failed to initialize LLM service: {e}")
            exit()
    
    def invoke(self, prompt: str) -> str:
        """Sends a prompt to the LLM and returns the response"""
        try:
            response = self.llm.invoke(prompt)
            return response.strip()
        except Exception as e:
            print(f"[Error]: An error occurred while invoking the LLM: {e}")
            return "I'm sorry, I seem to be having trouble thinking now"