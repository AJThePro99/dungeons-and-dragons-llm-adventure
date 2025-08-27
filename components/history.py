class ConversationHistory:
    def __init__(self):
        # History is a list of typles of (character_name, message)
        self.history = []
        
    def add_message(self, character_name: str, message: str):
        self.history.append((character_name, message))
        
    def get_formatted_history(self) -> str:
        if not self.history:
            return "The conversation has not started yet"
        
        # Formates the history in a readable format. e.g. "Sam: Hello friend!"        
        return "\n".join([f"{name}: {message}" for name, message in self.history])