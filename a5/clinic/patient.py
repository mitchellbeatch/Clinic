from clinic.dao.memory_note_dao import MemoryNoteDAO
from clinic.dao.note_dao_pickle import NoteDAOPickle

class Patient:
    def __init__(self, phn, name, birth_date, phone, email, address, autosave=False):
        self.phn = phn
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address
        self.note_dao = NoteDAOPickle(phn=phn, autosave=autosave) if autosave else MemoryNoteDAO()

    def add_note(self, text):
        return self.note_dao.create_note(text)

    def list_notes(self):
        return self.note_dao.list_notes()

    def __repr__(self):
        return f"Patient(phn={self.phn}, name='{self.name}')"

    def __eq__(self, other):
        if not isinstance(other, Patient):
            return False
        return (
            self.phn == other.phn and
            self.name == other.name and
            self.birth_date == other.birth_date and
            self.phone == other.phone and
            self.email == other.email and
            self.address == other.address
        )
