from datetime import datetime
from clinic.note import Note
from clinic.dao.note_dao_pickle import NoteDAOPickle
from clinic.dao.memory_note_dao import MemoryNoteDAO

class PatientRecord:
    # initializes for patient record class
    def __init__(self, autosave=False):
        self.note_dao = NoteDAOPickle() if autosave else MemoryNoteDAO()

    def create_note(self, text):
        return self.note_dao.create_note(text)
    
    def search_note(self, code):
        return self.note_dao.search_note(code)
    
    def retrieve_notes(self, search_text):
        return self.note_dao.retrieve_notes(search_text)
    
    def update_note(self, code, new_text):
        return self.note_dao.update_note(code, new_text)
    
    def  delete_note(self, code):
        return self.note_dao.delete_note(code)
    
    def list_notes(self):
        return self.note_dao.list_notes()
    
