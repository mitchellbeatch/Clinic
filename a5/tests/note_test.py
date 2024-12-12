import unittest
from datetime import datetime
from clinic.controller import Controller
from clinic.note import Note

class TestController(unittest.TestCase):
    def setUp(self):
        """Initialize a Controller instance before each test."""
        self.controller = Controller(users={"user": "clinic2024"})

    def test_create_note(self):
        # Expected notes for comparison
        expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
        expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
        expected_note_3 = Note(3, "Patient says high BP is controlled, 120x80 in general.")

        # Ensure notes cannot be created without login
        self.assertIsNone(self.controller.create_note_for_current_patient("Patient comes with headache and high blood pressure."),
                          "cannot add note without logging in")

        # Log in the user
        self.assertTrue(self.controller.login("user", "clinic2024"), "login correctly")

        # Ensure notes cannot be created without setting a current patient
        self.assertIsNone(self.controller.create_note_for_current_patient("Patient comes with headache and high blood pressure."),
                          "cannot add note without a valid current patient")

        # Create a patient and set them as the current patient
        self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", 
                                       "john.hancock@outlook.com", "5000 Douglas St, Saanich")
        self.controller.set_current_patient(9792225555)

        # Create first note and check if it matches expected data
        actual_note = self.controller.create_note_for_current_patient("Patient comes with headache and high blood pressure.")
        self.assertIsNotNone(actual_note, "note 1 was created and is valid")
        self.assertEqual(actual_note, expected_note_1, "note 1 was created and its data are correct")

        # Verify retrieval of the note
        actual_note = self.controller.retrieve_note_for_current_patient(1)
        self.assertIsNotNone(actual_note, "note created and retrieved cannot be null")
        self.assertEqual(actual_note, expected_note_1, "note 1 was created, retrieved and its data are correct")

        # Create additional notes and validate
        actual_note = self.controller.create_note_for_current_patient("Patient complains of a strong headache on the back of neck.")
        self.assertIsNotNone(actual_note, "note 2 was created and is valid")
        self.assertEqual(actual_note, expected_note_2, "note 2 was created and its data are correct")

        actual_note = self.controller.create_note_for_current_patient("Patient says high BP is controlled, 120x80 in general.")
        self.assertIsNotNone(actual_note, "note 3 was created and is valid")
        self.assertEqual(actual_note, expected_note_3, "note 3 was created and its data are correct")

        # Log in and create note
        self.controller.login("user", "clinic2024")
        self.controller.set_current_patient(9792225555)
        actual_note = self.controller.create_note_for_current_patient("Patient comes with headache and high blood pressure.")
        self.assertIsNotNone(actual_note, "note was created")
        self.assertEqual(actual_note.text, expected_note.text, "note text matches expected")

    def test_retrieve_notes(self):
        # Expected notes for retrieval tests
        expected_notes = [
            Note(1, "Patient comes with headache and high blood pressure."),
            Note(2, "Patient complains of a strong headache on the back of neck."),
            Note(4, "Patient feels general improvement and no more headaches.")
        ]

        # Log in and create a patient
        self.controller.login("user", "clinic2024")
        self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", 
                                       "john.hancock@outlook.com", "5000 Douglas St, Saanich")
        self.controller.set_current_patient(9792225555)

        # Add notes
        self.controller.create_note_for_current_patient("Patient comes with headache and high blood pressure.")
        self.controller.create_note_for_current_patient("Patient complains of a strong headache on the back of neck.")
        self.controller.create_note_for_current_patient("Patient is taking medicines to control blood pressure.")
        self.controller.create_note_for_current_patient("Patient feels general improvement and no more headaches.")
        
        # Retrieve notes by search term
        retrieved_notes = self.controller.retrieve_notes_by_text_for_current_patient("headache")
        self.assertEqual(len(retrieved_notes), 3, "retrieved list of headache notes has size 3")
        for i, expected_note in enumerate(expected_notes):
            self.assertEqual(retrieved_notes[i], expected_note, f"Note {i+1} matches expected note")

    def test_update_note(self):
        # Log in, create patient, and add notes
        self.controller.login("user", "clinic2024")
        self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", 
                                       "john.hancock@outlook.com", "5000 Douglas St, Saanich")
        self.controller.set_current_patient(9792225555)
        self.controller.create_note_for_current_patient("Patient is taking medicines to control blood pressure.")

        # Update a note
        updated_text = "Patient is taking Losartan 50mg to control blood pressure."
        self.assertTrue(self.controller.update_note_for_current_patient(1, updated_text), "note was updated successfully")
        updated_note = self.controller.retrieve_note_for_current_patient(1)
        self.assertEqual(updated_note.text, updated_text, "note text matches updated text")

    def test_delete_note(self):
        # Log in, create patient, add notes
        self.controller.login("user", "clinic2024")
        self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", 
                                       "john.hancock@outlook.com", "5000 Douglas St, Saanich")
        self.controller.set_current_patient(9792225555)
        self.controller.create_note_for_current_patient("Patient is taking medicines to control blood pressure.")

        # Delete a note and verify
        self.assertTrue(self.controller.delete_note_for_current_patient(1), "note was deleted successfully")
        deleted_note = self.controller.retrieve_note_for_current_patient(1)
        self.assertIsNone(deleted_note, "deleted note is no longer retrievable")

    def test_list_notes(self):
        # Log in, create patient, add multiple notes
        self.controller.login("user", "clinic2024")
        self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", 
                                       "john.hancock@outlook.com", "5000 Douglas St, Saanich")
        self.controller.set_current_patient(9792225555)
        self.controller.create_note_for_current_patient("Patient feels better today.")
        self.controller.create_note_for_current_patient("Patient has a mild headache in the evening.")

        # List notes and verify order
        notes_list = self.controller.list_notes_for_current_patient()
        self.assertEqual(len(notes_list), 2, "two notes are listed")
        self.assertEqual(notes_list[0].text, "Patient has a mild headache in the evening.")
        self.assertEqual(notes_list[1].text, "Patient feels better today.")

if __name__ == "__main__":
    unittest.main()
