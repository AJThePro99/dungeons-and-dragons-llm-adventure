from components.character import Participant, GameCharacter, DungeonMaster
from components.history import ConversationHistory
from components.llm_service import LLMService
from config import CAMPAIGN_TOPIC, DUNGEON_MASTER, HUMAN_PLAYER, PLAYER_SAM, PLAYER_ELLIE
import textwrap

class Orchestrator:
    def __init__(self):
        print(f"[Action]: Initializing Orchestrator")
        
        # self.history = ConversationHistory()
        # self.llm_service = LLMService()
        self.dm = DungeonMaster(dm = DUNGEON_MASTER)
        self.player_list = [
            PLAYER_ELLIE,                         
            HUMAN_PLAYER,
            PLAYER_SAM
         ]
        self.player_count = 4
        self.wrap_width = 80
        
    def wrapped_print(self, text):
        print(textwrap.fill(text, width=self.wrap_width))
        
        
    def pre_game_information(self):
        print("Pre game information")
        print(f"\t\t\t[Dungeon Master] {self.dm.dm.name}\n\n")
        self.wrapped_print(f"Campaign state: {CAMPAIGN_TOPIC}\n")
        
        for player in self.player_list:
            print(f"\t[Participant] \t{player.name}")
            
            print(f"\t[Character] \t{player.character.character_name}\n\t[Role] \t\t{player.character.character_role}")
            print("\n")
            
    def dm_introduction(self):
        
        pass
        
    def start_game(self):
        self.pre_game_information()
        self.dm_introduction()
        
        pass
        