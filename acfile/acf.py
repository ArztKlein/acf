from acfile import Section

class ACF:
    def __init__(self, variables: dict):
        self.variables = variables

        self.sections = {}

        for item in variables.items():
            section_key, section = item

            self.sections[section_key] = Section(section)

    
    def __getattr__(self, name) -> dict:
        assert name in self.sections, "Section does not exist"
        
        return self.sections[name]