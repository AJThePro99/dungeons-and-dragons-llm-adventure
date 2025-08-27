from components.character import Character
from components.history import ConversationHistory
from components.llm_service import LLMService
from config import CONVERSATION_TOPIC

class Orchestrator:
    """The main controller that manages the conversation flow"""
    def __init__(self):
        print(f"[Action]: Initializing Orchestrator")
        
        self.history = ConversationHistory()
        self.llm_service = LLMService()
        
        # Defining Personas
        
        dm_persona = "You are Hannah, the Dungeon Master. Your role is to set the scene and guide the conversation. You are mysterious and speak descriptively. You will start the conversation."
        sam_persona = "You are Sam, a witty and slightly cynical Rogue. You are practical, distrustful of magic, and always looking for a clear plan." # You are skeptical about the 'strange lights'.
        ellie_persona = "You are Ellie, a brave and optimistic Cleric. You are driven by your faith to help others and see the good in situations." # You believe the lights are a sign you must investigate.
        player_persona = "You are the player. You are a curious and adventurous Wizard. You are eager to understand the magical nature of the lights."
        
        # Creating character instances
        self.dm = Character(name="Hannah (DM)", persona=dm_persona)
        self.sam = Character(name="Sam", persona=sam_persona)
        self.ally = Character(name="Ellie", persona=ellie_persona)
        self.player = Character(name="Player", persona=player_persona, role="Human")
        
        # Setting up turn order
        self.turn_order = [self.dm, self.sam, self.player, self.ally]
        self.current_turn_index = 0
        
    def _build_prompt(self, character_to_act: Character) -> str:
        """Builds the final prompt to send to the LLM"""
        formatted_history = self.history.get_formatted_history()
        
        # prompt templating
        prompt = f"""
### INSTRUCTIONS ###
You are an actor playing a character in a conversation. Your character's name is {character_to_act.name}.
Your persona is: {character_to_act.persona}
The topic of the conversation is: {CONVERSATION_TOPIC}
Based on your persona and the history, provide the next response for {character_to_act.name}. Speak only as your character. Do not speak for anyone else. Keep your response to a few sentences.

### CONVERSATION HISTORY ###
{formatted_history}

### YOUR RESPONSE ###
{character_to_act.name}:
"""
        return prompt
    
    def start_conversation(self):
        """The main loop that runs the conversation"""
        print("\n === Starting Conversation Session ===")
        print(f"Topic: {CONVERSATION_TOPIC}\n")
        
        while True:
            # Determine whose turn it is
            current_character = self.turn_order[self.current_turn_index]
            response = ""
            
            if current_character.role == "Human":
                # Get input from human player
                try:
                    response = input(f"[{current_character.name}]: ").strip()
                    if response.lower() == "exit":
                        print("\nExiting conversation.\nGoodbye!")
                        break
                except KeyboardInterrupt: # Handling Ctrl + C
                    print("\nExiting conversation\nGoodbye!")
                    break
                
            else: # AI's turn
                print(f"\n[{current_character.name} is thinking...]")
                #Build the prompt and get the AI's response
                prompt  = self._build_prompt(current_character)
                response = self.llm_service.invoke(prompt)
                print(f"[{current_character.name}]: \n{response}]\n")
                
            # Add the response to the history and advance the turn
            
            if response:
                self.history.add_message(current_character, response)
                
            self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)