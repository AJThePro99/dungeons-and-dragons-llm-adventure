from components.character import Participant, GameCharacter
# === LLM Configuration ===
LLM_BASE_URL = "http://127.0.0.1:1234/v1"
LLM_API_KEY = "not-needed"
LLM_TEMPERATURE = 0.7

# === Conversation Configuration ===
CAMPAIGN_TOPIC = "You are all adventurers in a tavern, discussing the strange lights seen over the village last night. You are trying to decide if you should investigate."

# === Game Character Configuration ===
GAME_VALERIUS = GameCharacter(character_name="Valerius", character_role="Human Fighter")
GAME_ARIANA = GameCharacter(character_name="Ariana", character_role="Elf Mage")
GAME_HENRY = GameCharacter(character_name="Henry", character_role="Tiefling Bard")

# === Player Configurations ===
DUNGEON_MASTER = Participant(name="Hannah", personality="Fair, and chatty personality, with a strong talent for storytelling.", character="DUNGEON MASTER")
HUMAN_PLAYER = Participant(name="Aadith", personality="Realistic, and Logic Oriented man", character=GAME_VALERIUS)
PLAYER_SAM = Participant(name="Sam", personality="Charming, Flirty, and flowery with words, playful man", character=GAME_HENRY)
PLAYER_ELLIE = Participant(name="Ellie", personality="Kind, Curious, and protective woman", character=GAME_ARIANA)