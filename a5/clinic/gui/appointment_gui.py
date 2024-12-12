import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QDialog, QLabel, 
                             QMessageBox, QLineEdit, QPushButton, QVBoxLayout,
                             QToolBar, QTableView, QPlainTextEdit, QWidget, QStackedWidget,
                             QGroupBox, QHBoxLayout, QGridLayout)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from ..controller import Controller
from clinic.gui.login_gui import LoginDialog
import clinic.controller

class AppointmentDialog(QDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Medical Clinic System - Appointment Menu')
        self.setGeometry(500, 400, 300, 300)
        layout = QVBoxLayout()
        grid_layout = QGridLayout()
        
        patient = self.controller.get_current_patient()
        phn = patient.phn
        phn_label = QLabel(f"Appointment for PHN: {phn}")
        layout.addWidget(phn_label)

        add_note_button = QPushButton('Create Note to patient record')
        search_bar = QLineEdit(self)
        search_bar.setPlaceholderText("Retrieve Notes by text")
        search_button = QPushButton('Search')
        update_note_button = QPushButton('Update Note from patient record')
        delete_note_button = QPushButton('Remove note from patient record')
        list_notes_button = QPushButton('List Full patient record')
        end_appointment_button = QPushButton('Finish appointment')
        
        layout.addWidget(add_note_button)
        layout.addWidget(search_bar)
        layout.addWidget(search_button)
        grid_layout.addWidget(update_note_button, 0, 0)
        grid_layout.addWidget(delete_note_button, 0, 1)
        grid_layout.addWidget(list_notes_button, 1, 0)
        grid_layout.addWidget(end_appointment_button, 1, 1)
        self.setLayout(layout)
        layout.addLayout(grid_layout)

        add_note_button.clicked.connect(self.create_note_dialog)
        search_button.clicked.connect(self.retrieve_note_dialog)
        update_note_button.clicked.connect(self.update_note_dialog)
        delete_note_button.clicked.connect(self.delete_note_dialog)
        list_notes_button.clicked.connect(self.list_notes_dialog)
        end_appointment_button.clicked.connect(self.end_appointment)

    def list_notes_dialog(self):
        current_patient = self.controller.get_current_patient()
        if not current_patient: #error if no patient is selected
            QMessageBox.warning(self, "Error", "Select a patient first to create a note")
            return
        
        #dialog
        notes_dialog = QDialog(self)
        notes_dialog.setWindowTitle("Patient Record")
        notes_dialog.setModal(True)
        notes_dialog.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        patient_label = QLabel(f"Patient Record for: {current_patient.name} (PHN: {current_patient.phn})") 
        layout.addWidget(patient_label)

        #add notes in display area
        notes_display = QPlainTextEdit()
        notes_display.setReadOnly(True)
        layout.addWidget(notes_display)
        notes_dialog.setLayout(layout)

        try:
            notes = self.controller.list_notes()
            notes_display.clear()
            for note in notes:
                formatted_note = f"Note ID: {note.code}\n"
                formatted_note += f"Timestamp: {note.timestamp}\n"
                formatted_note += f"Text: {note.text}\n"
                formatted_note += "-" * 50 + "\n"
                notes_display.appendPlainText(formatted_note)
            notes_dialog.exec()
        except Exception as e:
            QMessageBox.warning(notes_dialog, "Error", str(e))

    def create_note_dialog(self):
        try:
            current_patient = self.controller.get_current_patient()
            if not current_patient: #error if no patient is selected
                QMessageBox.warning(self, "Error", "Select a patient first to create a note")
                return
            
            #dialog
            note_dialog = QDialog(self)
            note_dialog.setWindowTitle("Create Note")
            note_dialog.setModal(True)
            note_dialog.setGeometry(100, 100, 400, 300)
            layout = QVBoxLayout()

            #widgets
            note_label = QLabel(f"Creating note for patient: {current_patient.name}")
            note_text =  QPlainTextEdit()
            note_text.setPlaceholderText("Enter Note here...")
            create_button = QPushButton("Create Note")
            layout.addWidget(note_label)
            layout.addWidget(note_text)
            layout.addWidget(create_button)
            note_dialog.setLayout(layout)

            def create_note():
                try:
                    text = note_text.toPlainText()
                    if not text:
                        QMessageBox.warning(note_dialog, "Error", "Note text cannot be empty")
                        return
                    note = self.controller.create_note(text)
                    if note:
                        QMessageBox.information(note_dialog, "Success", "Note created successfully")
                        note_dialog.close()

                except Exception as e:
                    QMessageBox.warning(note_dialog, "Error", str(e))
            create_button.clicked.connect(create_note)
            note_dialog.exec()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def retrieve_note_dialog(self):
        notes_dialog = QDialog(self)
        notes_dialog.setWindowTitle("Patient Notes")
        notes_dialog.setModal(True)
        notes_dialog.setGeometry(100, 100, 600, 500)
        layout = QVBoxLayout()  

        current_patient = self.controller.get_current_patient()
        patient_label = QLabel(f"Notes for patient: {current_patient.name} (PHN: {current_patient.phn})") 
        layout.addWidget(patient_label)

        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search Notes...")
        search_button = QPushButton("Search")
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)

        #add notes in display area
        notes_display = QPlainTextEdit()
        notes_display.setReadOnly(True)
        notes_dialog.setMinimumHeight(300)
        layout.addWidget(notes_display)
        refresh_button = QPushButton("Refresh Notes")
        layout.addWidget(refresh_button)
        notes_dialog.setLayout(layout)

        def display_notes(search_text=""):
            try:
                notes_display.clear()
                if search_text:
                    notes = self.controller.retrieve_notes(search_text)
                else:
                    notes = self.controller.list_notes()
                if not notes:
                    notes_display.setPlainText("No notes found.")
                    return
                for note in notes:
                    formatted_note = f"Note ID: {note.code}\n"
                    formatted_note += f"Timestamp: {note.timestamp}\n"
                    formatted_note += f"Text: {note.text}\n"
                    formatted_note += "-" * 50 + "\n"
                    notes_display.appendPlainText(formatted_note)
            except Exception as e:
                QMessageBox.warning(notes_dialog, "Error", str(e))
        search_button.clicked.connect(lambda: display_notes(search_input.text()))
        search_input.returnPressed.connect(lambda: display_notes(search_input.text()))
        refresh_button.clicked.connect(lambda: display_notes())
        display_notes()
        notes_dialog.exec() 

    def update_note_dialog(self):
        current_patient = self.controller.get_current_patient()
        if not current_patient:
            QMessageBox.warning(self, "Error", "Please select a patient")
            return
        note_dialog = QDialog(self)
        note_dialog.setWindowTitle("Update Note")
        note_dialog.setModal(True)
        note_dialog.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        #widgets
        note_input = QLineEdit()
        note_input.setPlaceholderText("Enter Note ID")
        note_text = QPlainTextEdit()
        note_text.setPlaceholderText("Enter new note...")
        update_button = QPushButton("Update Note")

        layout.addWidget(QLabel("Note ID:"))
        layout.addWidget(note_input)
        layout.addWidget(QLabel("New Note Text:"))
        layout.addWidget(note_text)
        layout.addWidget(update_button)
        note_dialog.setLayout(layout)

        def update_note():
            try:
                note_id = int(note_input.text())
                text = note_text.toPlainText()

                if not text:
                    QMessageBox.warning(note_dialog, "Error", "Note text cannot be empty")
                    return
                if self.controller.update_note(note_id, text):
                    QMessageBox.information(note_dialog, "Success", "Note updated successfully")
                    note_dialog.close()
                else:
                    QMessageBox.warning(note_dialog, "Error", "Note not found")
            except ValueError:
                QMessageBox.warning(note_dialog, "Error", "Note not found")
            except Exception as e:
                QMessageBox.warning(note_dialog, "Error", str(e))
        update_button.clicked.connect(update_note)
        note_dialog.exec()

    def delete_note_dialog(self):
        current_patient = self.controller.get_current_patient()
        if not current_patient:
            QMessageBox.warning(self, "Error", "Please select a patient to delete.")
            return
        dialog = QDialog(self)
        dialog.setWindowTitle("Delete Note")
        dialog.setModal(True)
        dialog.setGeometry(100, 100, 300, 150)
        layout = QVBoxLayout()

        #widgets
        note_input = QLineEdit()
        note_input.setPlaceholderText("Enter Note ID")
        delete_button = QPushButton("Delete Note")

        #add widgets to layout
        layout.addWidget(QLabel("Note ID:"))
        layout.addWidget(note_input)
        layout.addWidget(delete_button)
        dialog.setLayout(layout)

        def delete_note():
            try:
                note_id = int(note_input.text())
                deletion = QMessageBox.question(
                    dialog, 
                    "Confirm Delete",
                    "Are you sure you want to delete this patient note?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if deletion == QMessageBox.StandardButton.Yes:
                    if self.controller.delete_note(note_id):
                        QMessageBox.information(dialog, "Success", "Note deleted successfully")
                        dialog.accept()
                    else:
                        QMessageBox.warning(dialog, "Error", "Note not found")
            except ValueError:
                QMessageBox.warning(dialog, "Error", "Please enter valid Note ID")
            except Exception as e:
                QMessageBox.warning(dialog, "Error", str(e))
        delete_button.clicked.connect(delete_note)
        dialog.exec()

    def end_appointment(self):
        self.close()