class Section:
    def __init__(self, values: dict):
        self.values = values
    
    def __getattr__(self, name) -> dict:
        return self.values[name]