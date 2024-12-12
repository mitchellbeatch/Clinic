from clinic.dao.note_dao import NoteDAO
from datetime import datetime
from clinic.note import Note

class MemoryNoteDAO(NoteDAO):
    def __init__(self):
        self.notes = {}
        self.note_counter = 0

    def search_note(self, key):
        return self.notes.get(key)

    def create_note(self, text):
        self.note_counter += 1
        note = Note(self.note_counter, text, datetime.now())
        self.notes[self.note_counter] = note
        return note

    def retrieve_notes(self, search_string):
        return [note for note in self.notes.values() 
                if search_string.lower() in note.text.lower()]

    def update_note(self, key, text):
        if key in self.notes:
            self.notes[key].text = text
            self.notes[key].timestamp = datetime.now()
            return True
        return False

    def delete_note(self, key):
        if key in self.notes:
            del self.notes[key]
            return True
        return False

    def list_notes(self):
        return sorted(list(self.notes.values()), 
                     key=lambda x: x.timestamp if x.timestamp else datetime.min,
                     reverse=True)