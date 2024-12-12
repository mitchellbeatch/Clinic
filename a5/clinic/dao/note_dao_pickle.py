import pickle
import os
from clinic.dao.note_dao import NoteDAO
from clinic.note import Note
from datetime import datetime

class NoteDAOPickle(NoteDAO):
    def __init__(self, phn=None, autosave=False):
        self.notes = {}
        self.note_counter = 0
        self.phn = phn
        self.autosave = autosave
        if autosave and phn:
            self.load_notes()

    def load_notes(self):
        """Load notes from the patient's record file."""
        try:
            filename = f'clinic/records/{self.phn}.dat'
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    data = pickle.load(f)
                    self.notes = data['notes']
                    # Update counter to highest note code
                    if self.notes:
                        self.note_counter = max(self.notes.keys())
        except (FileNotFoundError, pickle.UnpicklingError):
            self.notes = {}
            self.note_counter = 0

    def save_notes(self):
        """Save notes to the patient's record file."""
        if self.autosave and self.phn:
            if not os.path.exists('clinic/records'):
                os.makedirs('clinic/records')
            filename = f'clinic/records/{self.phn}.dat'
            with open(filename, 'wb') as f:
                pickle.dump({
                    'notes': self.notes,
                    'counter': self.note_counter
                }, f)

    def create_note(self, text):
        """Create a new note and save it."""
        self.note_counter += 1
        note = Note(self.note_counter, text)
        self.notes[self.note_counter] = note
        if self.autosave:
            self.save_notes()
        return note

    def update_note(self, key, text):
        """Update an existing note and save changes."""
        if key in self.notes:
            note = Note(key, text)
            self.notes[key] = note
            if self.autosave:
                self.save_notes()
            return True
        return False

    def delete_note(self, key):
        """Delete a note and save changes."""
        if key in self.notes:
            del self.notes[key]
            if self.autosave:
                self.save_notes()
            return True
        return False

    def search_note(self, key):
        """Search for a note by its key."""
        return self.notes.get(key)

    def list_notes(self):
        """Return a list of all notes in reverse chronological order."""
        return sorted(self.notes.values(), key=lambda x: x.code, reverse=True)

    def retrieve_notes(self, search_string):
        """Retrieve all notes containing the search string."""
        return sorted([note for note in self.notes.values() 
                      if search_string.lower() in note.text.lower()],
                     key=lambda x: x.code)