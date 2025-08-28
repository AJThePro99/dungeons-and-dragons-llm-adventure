class ConversationHistory:
    def __init__(self, max_rounds=5):
        self.rounds = []
        self.current_round = []
        self.max_rounds = max_rounds
        self.dm_narration = None
        
    def add_message(self, current_player:str, game_character_name: str, message: str):
       
        if "Dungeon Master" in current_player:
            self.dm_narration = (current_player, game_character_name, message)
            # We don't add DM narration to the current round, as DM is not a participant
            return
            
        # Add player message to the current round
        self.current_round.append((current_player, game_character_name, message))
        
        # Check if the current round is complete (all players have spoken)
        if len(self.current_round) >= 3:  # Assuming 3 players
            self.rounds.append(self.current_round)
            self.current_round = []
            
            if len(self.rounds) > self.max_rounds:
                self.rounds = self.rounds[-self.max_rounds:]
        
    def get_formatted_history(self) -> str:
        """Returns a nicely formatted history for display to users"""
        if not self.rounds and not self.current_round:
            return "The conversation has not started yet"
        
        formatted = []
        
        if self.dm_narration:
            formatted.append(f"[DM] {self.dm_narration[2]}")
            formatted.append("")
        
        for i, round_messages in enumerate(self.rounds):
            for current_player, game_character_name, message in round_messages:
                formatted.append(f"[{game_character_name}] {message}")
                formatted.append("")
        
        for current_player, game_character_name, message in self.current_round:
            formatted.append(f"[{game_character_name}] {message}")
            formatted.append("")
        
        return "\n".join(formatted)
    
    def get_llm_friendly_history(self) -> str:
        """Returns a concise, LLM-friendly version of the history optimized for prompts"""
        if not self.rounds and not self.current_round and not self.dm_narration:
            return "No previous conversation."
            
        formatted_messages = []
        
        if self.dm_narration:
            formatted_messages.append(f"Narrator: {self.dm_narration[2]}")
        
        # Include all messages from the most recent rounds
        for round_messages in self.rounds:
            for current_player, game_character_name, message in round_messages:
                formatted_messages.append(f"{game_character_name}: {message}")
        
        # Include messages from the current round
        for current_player, game_character_name, message in self.current_round:
            formatted_messages.append(f"{game_character_name}: {message}")
                
        return "\n".join(formatted_messages)
        
    def get_all_messages(self):
        """Returns all messages from all rounds including the current round"""
        all_messages = []
        if self.dm_narration:
            all_messages.append(self.dm_narration)
            
        for round_messages in self.rounds:
            all_messages.extend(round_messages)
        all_messages.extend(self.current_round)
        return all_messages