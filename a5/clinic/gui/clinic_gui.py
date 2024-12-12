import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QDialog, QLabel, 
                             QMessageBox, QLineEdit, QPushButton, QVBoxLayout,
                             QToolBar, QTableView, QPlainTextEdit, QWidget, QStackedWidget,
                             QGroupBox, QHBoxLayout)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from ..controller import Controller, InvalidLoginException, IllegalAccessException, IllegalOperationException
from clinic.gui.login_gui import LoginDialog
import clinic.controller
from clinic.gui.appointment_gui import AppointmentDialog

class ClinicGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.controller = Controller(autosave=True)
        self.login = LoginDialog(self.controller)
        self.login.exec()
        if QDialog.DialogCode.Accepted:
            self.close()
            self.init_ui()
            self.show()
        else:
            sys.exit

    def init_ui(self):
        self.setWindowTitle("Medical Clinic Application")
        self.setGeometry(100, 100, 800, 600)

        #creating a widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        #create menu bar
        self.create_menu_bar()

        #search bar for patient
        search_layout = QVBoxLayout()
        search_label =QLabel("Search Patients:")
        search_input_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.phn_input = QLineEdit()
        self.phn_input.setPlaceholderText("Enter PHN to search")
        self.search_input.setPlaceholderText("Enter patient name to search")
        search_button = QPushButton("Search")
        search_input_layout.addWidget(self.phn_input)
        search_input_layout.addWidget(self.search_input)
        search_input_layout.addWidget(search_button)
        search_layout.addWidget(search_label)
        search_layout.addLayout(search_input_layout)
        main_layout.addLayout(search_layout)
        search_button.clicked.connect(self.perform_search)
        self.search_input.returnPressed.connect(self.perform_search) 
        self.phn_input.returnPressed.connect(self.perform_search)

        #adds patient table
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['PHN', 'Name', 'Birth Date', 
                                              'Phone Number', 'Emaail', 'Address'])
        self.table_view.setModel(self.model)
        main_layout.addWidget(self.table_view)
        self.table_view.clicked.connect(self.on_patient_selected)

        #add current patient info
        self.current_patient_group = QGroupBox("Current Patient")
        current_patient_layout = QVBoxLayout()
        self.current_patient_label = QLabel("No Patient Selected")
        current_patient_layout.addWidget(self.current_patient_label)
        self.current_patient_group.setLayout(current_patient_layout)
        main_layout.addWidget(self.current_patient_group)
        self.update_patient_table()   #initial population of table
    
        #add start appointment button
        self.status_label = QLabel("")
        self.start_appointment_button = QPushButton("Start Appointment")
        self.start_appointment_button.clicked.connect(self.start_appointment)
        current_patient_layout.addWidget(self.start_appointment_button)
        current_patient_layout.addWidget(self.status_label)

        #add end appointment button
        self.end_appointment_button = QPushButton("End Appointment")
        current_patient_layout.addWidget(self.end_appointment_button)
        self.end_appointment_button.clicked.connect(self.end_appointment)

    def end_appointment(self):
        try:
            if self.controller.get_current_patient():
                self.controller.unset_current_patient()
                self.status_label.setText("Appointment has ended.")
            else:
                self.status_label.setText("There is no active appointment.")
        except Exception as e:
            self.status_label.setText("Appointment could not be closed.")

    def start_appointment(self):
        try:
            patient = self.controller.get_current_patient()
            phn = patient.phn
            if self.controller.set_current_patient(phn):
                self.status_label.setText('Appointment started for PHN: ' + str(phn))
                self.AppointmentDialog = AppointmentDialog(self.controller)
                self.AppointmentDialog.exec()
            else:
                self.status_label.setText('Failed to start appointment.')
        except ValueError:
            self.status_label.setText("Please enter a valid PHN (numbers only).")
        except Exception as e:
            self.status_label.setText(str(e))

    def create_menu_bar(self):  
        menubar = self.menuBar()

        #create file menu
        file_menu = menubar.addMenu('Menu')

        #logout action for menu
        logout_action = file_menu.addAction('Logout')
        logout_action.triggered.connect(self.logout)
        file_menu.addSeparator()
        #exit action after logout
        exit_action = file_menu.addAction('Exit')
        exit_action.triggered.connect(self.close)
        
        #create function
        file_menu.addSeparator
        create_action = file_menu.addAction("Create Patient")
        create_action.triggered.connect(self.show_create_dialog)

        #retrieve function
        file_menu.addSeparator
        retrieve_action = file_menu.addAction("Retrieve Patient")
        retrieve_action.triggered.connect(self.show_retrieve_dialog)

        #update function
        file_menu.addSeparator
        update_action = file_menu.addAction("Update Patient")
        update_action.triggered.connect(self.update_patient_dialog)

        #delete function
        file_menu.addSeparator
        delete_action = file_menu.addAction("Delete Patient")
        delete_action.triggered.connect(self.delete_patient_dialog)

    def logout(self):
        try:
            if self.controller.logout():
                self.close()
                if not self.login.remember_box.isChecked():
                    self.login.username_input.setText("")
                    self.login.password_input.setText("")
            self.login.exec()
        except Exception as e:
            print(str(e))
            QMessageBox.warning(self, "Error", str(e))
        if QDialog.DialogCode.Accepted:
            self.login.close()
        self.show()
    
    def perform_search(self):
        try:
            search_text = self.search_input.text()
            phn_text = self.phn_input.text()
            self.update_patient_table(search_text)
            self.model.removeRows(0, self.model.rowCount()) #clears table
            
            if phn_text:
                try:
                    phn = int(phn_text)
                    patient = self.controller.search_patient(phn)
                    if patient:
                        row = [
                            QStandardItem(str(patient.phn)),
                            QStandardItem(str(patient.name)),
                            QStandardItem(str(patient.birth_date)),
                            QStandardItem(str(patient.phone)),
                            QStandardItem(str(patient.email)),
                            QStandardItem(str(patient.address)),
                        ]
                        self.model.appendRow(row)
                    else:
                        QMessageBox.warning(self, "Not found", "No patient with that PHN")
                except ValueError:
                    QMessageBox.warning(self, "Error", "Please enter valid PHN")
            elif search_text:   #search name if field not empty
                patients = self.controller.retrieve_patients(search_text)
                for patient in patients:
                    row = [
                        QStandardItem(str(patient.phn)),
                        QStandardItem(str(patient.name)),
                        QStandardItem(str(patient.birth_date)),
                        QStandardItem(str(patient.phone)),
                        QStandardItem(str(patient.email)),
                        QStandardItem(str(patient.address)),
                    ]
                    self.model.appendRow(row)
            else:   #if both fields empty show all patients
                patients = self.controller.list_patients()
                for patient in patients:
                    row = [
                        QStandardItem(str(patient.phn)),
                            QStandardItem(str(patient.name)),
                            QStandardItem(str(patient.birth_date)),
                            QStandardItem(str(patient.phone)),
                            QStandardItem(str(patient.email)),
                            QStandardItem(str(patient.address)),
                    ]
                    self.model.appendRow(row)
            self.table_view.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def show_create_dialog(self):
        #make the create dialog
        create_dialog = QDialog(self)
        create_dialog.setWindowTitle("Create Patient")
        create_dialog.setModal(True)
        create_dialog.setGeometry(100, 100, 250, 100)
        #create layout
        layout = QVBoxLayout()
        #create widgets
        phn_input = QLineEdit()
        phn_input.setPlaceholderText("Enter PHN")
        name_input = QLineEdit()
        name_input.setPlaceholderText("Enter name of patient")
        birth_date_input = QLineEdit()
        birth_date_input.setPlaceholderText("Enter birth date (YYYY-MM-DD)")
        phone_input = QLineEdit()
        phone_input.setPlaceholderText("Enter phone number")
        email_input = QLineEdit()
        email_input.setPlaceholderText("Enter email")
        address_input = QLineEdit()
        address_input.setPlaceholderText("Enter address")
        #create button
        submit_button = QPushButton("Create Patient")
        #add widgets to layout
        layout.addWidget(QLabel("PHN:"))
        layout.addWidget(phn_input)
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(name_input)
        layout.addWidget(QLabel("Birth Date:"))
        layout.addWidget(birth_date_input)
        layout.addWidget(QLabel("Phone Number:"))
        layout.addWidget(phone_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(email_input)
        layout.addWidget(QLabel("Address:"))
        layout.addWidget(address_input)
        layout.addWidget(submit_button)
        #set dialog layout
        create_dialog.setLayout(layout)

        def create_patient():
            try:
                phn = int(phn_input.text())
                name = name_input.text()
                birth_date = birth_date_input.text()
                phone = phone_input.text()
                email = email_input.text()
                address = address_input.text()
                patient = self.controller.create_patient(phn, name, birth_date,
                                                         phone, email, address)
                if patient:
                    QMessageBox.information(create_dialog,"Success", "Patient Created")
                    self.update_patient_table()
                    create_dialog.accept()
            except ValueError:
                QMessageBox.warning(create_dialog, "Error", "Please enter a valid PHN")
            except IllegalAccessException:
                print('\nMUST LOGIN FIRST.')
            except IllegalOperationException:
                print('\nERROR ADDING NEW PATIENT.') 
                print('There is a patient already registered with PHN %d.' % phn)
            except Exception as e:
                QMessageBox.warning(create_dialog, "Error", str(e))
        submit_button.clicked.connect(create_patient)
        create_dialog.exec()

    def show_retrieve_dialog(self):
        retrieve_dialog = QDialog(self)
        retrieve_dialog.setWindowTitle("Retrieve Patients")
        retrieve_dialog.setModal(True)
        retrieve_dialog.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        #create search input
        search_input = QLineEdit()
        search_input.setPlaceholderText("Enter name to search")

        #create table view
        table_view = QTableView()
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['PHN', 'Name', 'Birth Date', 
                                        'Phone Number', 'Email', 'Address'])
        table_view.setModel(model)

        #widgets
        layout.addWidget(QLabel("Search by name:"))
        layout.addWidget(search_input)
        layout.addWidget(table_view)
        retrieve_dialog.setLayout(layout)

        def update_table(search_text=""):
            model.removeRows(0, model.rowCount()) #this clears existing items
            try:
                if search_text:
                    patients = self.controller.retrieve_patients(search_text)
                else:
                    patients = self.controller.list_patients()
                for patient in patients:
                    row = [
                        QStandardItem(str(patient.phn)),
                        QStandardItem(str(patient.name)),
                        QStandardItem(str(patient.birth_date)),
                        QStandardItem(str(patient.phone)),
                        QStandardItem(str(patient.email)),
                        QStandardItem(str(patient.address)),
                    ]
                    model.appendRow(row)
                #resize column
                table_view.resizeColumnsToContents()
            except Exception as e:
                QMessageBox.warning(retrieve_dialog, "Error", str(e))
        search_input.textChanged.connect(update_table)
        update_table()
        retrieve_dialog.exec()

    def update_patient_table(self, search_text=""):
        self.model.removeRows(0, self.model.rowCount())
        try:
            if search_text:
                patients = self.controller.retrieve_patients(search_text)
            else:
                patients = self.controller.list_patients()
            for patient in patients:
                row = [
                    QStandardItem(str(patient.phn)),
                    QStandardItem(str(patient.name)),
                    QStandardItem(str(patient.birth_date)),
                    QStandardItem(str(patient.phone)),
                    QStandardItem(str(patient.email)),
                    QStandardItem(str(patient.address)),
                ]
                self.model.appendRow(row)
            self.table_view.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def on_patient_selected(self, index):
        phn = int(self.model.item(index.row(), 0).text())
        try: 
            self.controller.set_current_patient(phn)
            patient = self.controller.get_current_patient()
            if patient:
                self.current_patient_label.setText(
                    f"Selected Patient:\nPHN: {patient.phn}\n"
                f"Name: {patient.name}\n"
                f"Birth Date: {patient.birth_date}\n"
                f"Phone: {patient.phone}\n"
                f"Email: {patient.email}\n"
                f"Address: {patient.address}"
                )
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def update_patient_dialog(self):
        current_patient = self.controller.get_current_patient()
        if not current_patient:
            QMessageBox.warning(self, "Error", "Please select a patient")
            return
        #update dialog
        update_dialog = QDialog(self)
        update_dialog.setWindowTitle("Update Patient")
        update_dialog.setModal(True)
        update_dialog.setGeometry(100, 100, 300, 400)
        layout = QVBoxLayout()
        #widgets with current patient info
        phn_input = QLineEdit(str(current_patient.phn))
        name_input = QLineEdit(str(current_patient.name))
        birth_date_input = QLineEdit(str(current_patient.birth_date))
        phone_input = QLineEdit(str(current_patient.phone))
        email_input = QLineEdit(str(current_patient.email))
        address_input = QLineEdit(str(current_patient.address))
        update_button = QPushButton("Update Patient")
        #widgets to layout
        layout.addWidget(QLabel("PHN:"))
        layout.addWidget(phn_input)
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(name_input)
        layout.addWidget(QLabel("Birth Date:"))
        layout.addWidget(birth_date_input)
        layout.addWidget(QLabel("Phone Number:"))
        layout.addWidget(phone_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(email_input)
        layout.addWidget(QLabel("Address:"))
        layout.addWidget(address_input)
        layout.addWidget(update_button)
        #set dialog layout
        update_dialog.setLayout(layout)

        def update_patient():
            try:
                new_phn = int(phn_input.text())
                name = name_input.text()
                birth_date = birth_date_input.text()
                phone = phone_input.text()
                email = email_input.text()
                address = address_input.text()
                self.controller.unset_current_patient()
                #update the patient using controller
                updated_patient = self.controller.update_patient(
                    current_patient.phn,     #this is the old phn
                    new_phn,
                    name,
                    birth_date,
                    phone,
                    email,
                    address
                )
                if updated_patient:
                    QMessageBox.information(update_dialog, "Success", "Patient Updated")
                    self.update_patient_table() #to refresh table
                    update_dialog.accept()
            except ValueError:
                QMessageBox.warning(update_dialog, "Error", "Please enter a valid PHN")
            except IllegalOperationException:
                QMessageBox.warning(update_dialog, "Error", "Cannot Update Current patient")
            except Exception as e:
                QMessageBox.warning(update_dialog, "Error", str(e))
        update_button.clicked.connect(update_patient)
        update_dialog.exec()

    def delete_patient_dialog(self):
        #check if a patient is selected
        current_patient = self.controller.get_current_patient()
        if not current_patient:
            QMessageBox.warning(self, "Error", "Please select a patient to delete")
            return
        confirm = QMessageBox.question(
            self, 
            "Confirm Deletion",
            f"Are you sure you want to delete patient:\n\n"
            f"PHN: {current_patient.phn}\n"
            f"Name: {current_patient.name}\n"
            f"Birth Date: {current_patient.birth_date}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                self.controller.unset_current_patient()
                #delete patient
                if self.controller.delete_patient(current_patient.phn):
                    QMessageBox.information(self, "Success", "Patient deleted successfully")
                    self.current_patient_label.setText("No Patient Selected")
                    self.update_patient_table()
            except IllegalOperationException:
                QMessageBox.warning(self, "Error", "Cannot delete current patient")
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()

if __name__ == '__main__':  
    main()
