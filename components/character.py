class Character:
    def __init__(self, name: str, persona: str, role: str = "All"):
        self.name = name
        self.persona = persona
        self.role = role # Can be 'AI' or 'Human'