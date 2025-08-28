class DungeonMaster:
    def __init__(self, dm):
        self.dm = dm

class Participant:
    def __init__(self, name: str, personality: str, character):
        self.name = name
        self.personality = personality
        self.character = character
    
class GameCharacter:
    def __init__(self, character_name: str, character_role: str):
        self.character_name = character_name
        self.character_role = character_role