from acfile import Section

class ACF:
    def __init__(self, variables: dict):
        self.variables = variables

        self._sections = {}

        for item in variables.items():
            section_key, section = item

            self._sections[section_key] = Section(section)

    
    def __getattr__(self, name) -> dict:
        assert name in self._sections, "Section does not exist"
        
        return self._sections[name]

    @property
    def sections(self) -> dict:
        return self._sections