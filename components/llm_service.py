from langchain_openai import OpenAI
from config import LLM_BASE_URL, LLM_API_KEY, LLM_TEMPERATURE
import re

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
    
    def clean_response(self, text: str) -> str:
        """Cleans any model-specific artifacts from the response"""
        analysis_patterns = [
            r'We need .*? words',
            r'Let\'s craft ~\d+ words',
            r'Need to output',
            r'Let\'s do ~\d+ words',
            r'<\|channel\|>.*?<\|message\|>',
            r'<\|end\|>',
            r'<\|start\|>',
            r'No quotation marks',
            r'no quotes',
            r'no dialogue',
            r'assistant<\|channel\|>final<\|message\|>'
        ]
        
        contains_reasoning = any(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in analysis_patterns)
        
        if contains_reasoning:
            # Try to find the final message section
            final_message_match = re.search(r'<\|channel\|>final<\|message\|>(.*?)(?:<\|end\|>|$)', text, re.DOTALL)
            if final_message_match:
                return final_message_match.group(1).strip()
            
            # If that doesn't work, try to remove the reasoning sections
            # Look for lines that contain internal reasoning instructions
            lines = text.split('\n')
            filtered_lines = []
            in_reasoning = False
            
            for line in lines:
                # Check if line contains reasoning markers
                if any(re.search(pattern, line, re.IGNORECASE) for pattern in analysis_patterns):
                    in_reasoning = True
                    continue
                
                if not in_reasoning:
                    filtered_lines.append(line)
                else:
                    if not line.strip():
                        in_reasoning = False
            
            # If we found any valid content
            if filtered_lines:
                return '\n'.join(filtered_lines).strip()
        
        # If no reasoning patterns found or couldn't extract, return original with basic cleanup
        return text.strip()
    
    def invoke(self, prompt: str) -> str:
        """Sends a prompt to the LLM and returns the response"""
        try:
            response = self.llm.invoke(prompt)
            cleaned_response = self.clean_response(response)
            return cleaned_response.strip()
        except Exception as e:
            print(f"[Error]: An error occurred while invoking the LLM: {e}")
            return "I'm sorry, I seem to be having trouble thinking now"