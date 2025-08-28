from components.character import Participant, GameCharacter, DungeonMaster
from components.history import ConversationHistory
from components.llm_service import LLMService
from config import CAMPAIGN_TOPIC, DUNGEON_MASTER, HUMAN_PLAYER, PLAYER_SAM, PLAYER_ELLIE
import textwrap
import os
import re

class Orchestrator:
    def __init__(self):
        print(f"[Action]: Initializing Orchestrator")
        
        self.history = ConversationHistory(max_rounds=5)  # Keep only the most recent 5 rounds
        self.llm_service = LLMService()
        self.dm = DungeonMaster(dm = DUNGEON_MASTER)
        self.player_list = [
            PLAYER_ELLIE,
            HUMAN_PLAYER,
            PLAYER_SAM
         ]
                
        self.wrap_width = 80
        self.player_count = 3
        self.player_index = 0
        
    def wrapped_print(self, text, prefix=""):
        """Print text wrapped to the specified width with an optional prefix"""
        for line in text.split('\n'):
            print(prefix + textwrap.fill(line, width=self.wrap_width - len(prefix)))
    
    def print_separator(self, length=80):
        print("-" * length)
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def post_process_response(self, text):
        """Additional cleaning of model outputs to catch reasoning that wasn't cleaned"""
        reasoning_patterns = [
            r'We need .*? words',
            r'Let\'s craft ~\d+ words',
            r'Need to output',
            r'Let\'s do ~\d+ words',
            r'No quotation marks',
            r'no quotes',
            r'no dialogue',
            r'craft',
            r'output',
            r'instructions'
        ]
        
        lines = text.split('\n')
        filtered_lines = []
        
        for line in lines:
            # Skip lines that match any reasoning pattern
            if any(re.search(pattern, line, re.IGNORECASE) for pattern in reasoning_patterns):
                continue
            filtered_lines.append(line)
            
        return '\n'.join(filtered_lines).strip()
        
    def pre_game_information(self):
        self.clear_screen()
        self.print_separator()
        print("DUNGEONS & DRAGONS ADVENTURE")
        self.print_separator()
        print(f"\n[Dungeon Master]: {self.dm.dm.name}\n")
        self.wrapped_print(f"Campaign Setting: {CAMPAIGN_TOPIC}\n")
        
        print("PLAYERS & CHARACTERS:")
        for player in self.player_list:
            print(f"• {player.name} playing as {player.character.character_name} ({player.character.character_role})")
        print()
            
    def dm_introduction(self):
        self.print_separator()
        print("Scene Setting")
        self.print_separator()
        
        # Create a prompt for the DM's introduction
        players_info = "\n".join([
            f"- {p.name} playing as {p.character.character_name} ({p.character.character_role})" 
            for p in self.player_list
        ])
        
        prompt = f"""
        You are a narrator for a Dungeons & Dragons game, setting the scene with the following details:
        
        Campaign Setting:
        {CAMPAIGN_TOPIC}
        
        Players in the game:
        {players_info}
        
        Write a brief, engaging introduction to set the scene for this campaign. Describe the tavern, 
        the village, and mention the strange lights that were seen last night. End with a description
        that invites the players to start discussing.
        
        Important instructions:
        - Keep it under 150 words
        - Do not include any dialogue or quotes
        - Do not include any reasoning about how you're constructing the response
        - You are purely describing the scene and environment
        - Respond in a simple paragraph format without any meta-commentary
        """
        
        introduction = self.llm_service.invoke(prompt)
        introduction = self.post_process_response(introduction)
        print()
        self.wrapped_print(introduction)
        print()
        
        self.history.add_message(f"Dungeon Master {self.dm.dm.name}", "DM", introduction)
    
    def dm_narration(self, after_player=None):
        """Provide narration after a player's turn"""
        # Create a prompt for the DM's ongoing narration
        players_info = "\n".join([
            f"- {p.name} playing as {p.character.character_name} ({p.character.character_role})" 
            for p in self.player_list
        ])
        
        # Include the name of the player who just spoke if provided
        player_context = ""
        if after_player:
            player_context = f"This narration follows after {after_player.character.character_name}'s statement."
        
        prompt = f"""
        You are a narrator for a Dungeons & Dragons game. Your job is to describe the environment and setting after a character has spoken.
        
        Campaign Setting:
        {CAMPAIGN_TOPIC}
        
        Players in the game:
        {players_info}
        
        {player_context}
        
        Conversation History:
        {self.history.get_llm_friendly_history()}
        
        Based on the conversation so far, provide a short narration that builds atmosphere and describes the environment.
        
        Important instructions:
        - Describe what's happening around the players based on the most recent conversation
        - Only describe the scene, weather, atmosphere, and environment
        - Do not speak to the players directly
        - Do not include any dialogue
        - Do not ask questions
        - Do not provide guidance to the players
        - Keep your response under 80 words
        - Focus on visual and sensory details that relate to what was just discussed
        - Do not include any meta-commentary or reasoning about your response
        """
        
        response = self.llm_service.invoke(prompt)
        response = self.post_process_response(response)
        
        if response and response.strip().upper() != "SKIP":
            self.print_separator()
            print(f"[Hannah the Dungeon Master]")
            self.wrapped_print(response)
            print()
            self.history.add_message(f"Dungeon Master {self.dm.dm.name}", "DM", response)
        
    def display_history(self):
        """Display the conversation history when requested"""
        self.print_separator()
        print("CONVERSATION HISTORY (LAST 5 ROUNDS)")
        self.print_separator()
        
        all_messages = self.history.get_all_messages()
        
        for player, character, message in all_messages:
            if "Dungeon Master" in player:
                print(f"[Hannah the Dungeon Master]")
                self.wrapped_print(message)
            else:
                print(f"[{character}]")
                self.wrapped_print(message)
            print()
            
    def start_game(self):
        self.pre_game_information()
        self.dm_introduction()
        
        while True:
            current_player = self.player_list[self.player_index]
            
            self.print_separator()
            
            if current_player.name == "Human_Player":  # Human player
                print(f"YOUR TURN as [{current_player.character.character_name} | {current_player.character.character_role}]")
                self.print_separator()
                
                response = input("Type your response: ")
                
                # Check for special commands
                if response.strip().lower() == 'exit':
                    print("\nExiting game. Goodbye!")
                    return
                elif response.strip().lower() == 'history':
                    self.display_history()
                    continue
                
                print()
                print(f"[{current_player.character.character_name}]")
                self.wrapped_print(response)
                print()
            else:
                # AI player's turn
                print(f"[{current_player.character.character_name} | {current_player.character.character_role}]")
                self.print_separator()
                
                # Get information about other players for context
                other_players = [p for p in self.player_list if p.name != current_player.name]
                other_players_info = "\n".join([
                    f"- {p.name} playing as {p.character.character_name} ({p.character.character_role})" 
                    for p in other_players
                ])
                
                prompt = f"""
                You are roleplaying as {current_player.character.character_name}, a {current_player.character.character_role}.
                
                Character Information:
                - Your name: {current_player.character.character_name}
                - Your role: {current_player.character.character_role}
                - Your personality: {current_player.personality}
                
                Campaign Setting:
                {CAMPAIGN_TOPIC}
                
                Other Participants:
                {other_players_info}
                
                Conversation History:
                {self.history.get_llm_friendly_history()}
                
                Important instructions:
                - Respond directly as {current_player.character.character_name} without any meta-commentary
                - Write in first person as if you are the character speaking
                - Include appropriate dialogue with quotation marks
                - Stay in character and be conversational
                - Don't include any reasoning about how you're constructing the response
                - Don't prefix your response with your character name
                - Don't explain what you're doing - just do it
                - Keep your response under 150 words
                """
                response = self.llm_service.invoke(prompt)
                response = self.post_process_response(response)
                
                self.wrapped_print(response)
                print()
                
            if response:
                self.history.add_message(current_player.name, current_player.character.character_name, response)
                
                self.dm_narration(after_player=current_player)
                
            self.player_index = (self.player_index + 1) % self.player_count
        
        