class Note:
    def  __init__(self, code, text, timestamp=None):
        self.code = code
        self.text = text
        self.timestamp = timestamp

    def __eq__(self, other):
        if isinstance(other, Note):
            return (self.code == other.code and self.text == other.text)
        return False
    
    def __repr__(self):
        return  f"Note(code={self.code}, text={self.text}, timestamp={self.timestamp})"