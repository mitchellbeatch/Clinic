from functools import wraps
from clinic.dao.memory_patient_dao import MemoryPatientDAO
from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.patient import Patient
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

def check_login(func):
    @wraps(func)
    def check(self, *args):
        if not self.current_user:
            raise IllegalAccessException
        return func(self, *args)
    return check

class Controller:
    def __init__(self, users=None, autosave=False):
        self.current_user = None
        self.current_patient = None
        self.autosave = autosave
        self.user_data = {}

        if autosave:
            try:
                with open('clinic/users.txt', 'r') as f:
                    for line in f:
                        username, password_hash = line.strip().split(',')
                        self.user_data[username] = password_hash
            except FileNotFoundError: #back to default users if file nto found
                self.user_data = {
                    "user" : "123456",
                    "doctor" : "password123",
                    "admin" : "adminpass",
                    "ali" : "@G00dPassw0rd"
                }
        else:
            self.user_data = users if users else{
                "user": "123456",
                "doctor": "password123",
                "admin": "adminpass",
                "ali": "@G00dPassw0rd"
            }
        self.patient_dao = PatientDAOJSON(autosave) if autosave else MemoryPatientDAO()

    def login(self, username, password):
        if self.current_user:
            raise DuplicateLoginException
        if self.autosave:
            #use hashed passwords when autosave is True
            import hashlib
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if username in self.user_data and self.user_data[username] == hashed_password:
                self.current_user = username
                self.log_status = True
                return True
        else:
            #use plain text passwords when autosave is False
            if username in self.user_data and self.user_data[username] == password:
                self.current_user = username
                return True
        raise InvalidLoginException

    def logout(self):
        if not self.current_user:
            raise InvalidLogoutException
        self.current_user = None
        self.current_patient = None
        return True

    @check_login
    def search_patient(self, phn):
        return self.patient_dao.search_patient(phn)

    @check_login
    def create_patient(self, phn, name, birth_date, phone, email, address):
        if self.search_patient(phn):
            raise IllegalOperationException
        patient = Patient(phn, name, birth_date, phone, email, address)
        if self.patient_dao.create_patient(patient):
            return patient
        raise IllegalOperationException
    
    @check_login
    def retrieve_patients(self, search_string):
        return self.patient_dao.retrieve_patients(search_string)

    @check_login
    def update_patient(self, old_phn, new_phn, name, birth_date, phone, email, address):
        #check if trying to update current patient
        if self.current_patient and self.current_patient.phn == old_phn:
            raise IllegalOperationException 
        #first check if the original patient exists
        if not self.search_patient(old_phn):
            raise IllegalOperationException   
        #if old_phn and new_phn are different, check if new_phn already exists
        if old_phn != new_phn and self.search_patient(new_phn):
            raise IllegalOperationException 
        new_patient = Patient(new_phn, name, birth_date, phone, email, address, autosave=self.autosave)
        #update the patient in the DAO
        if self.patient_dao.update_patient(old_phn, new_patient):
            #if PHN changed, update the key in the patients dictionary
            if old_phn != new_phn:
                self.patient_dao.patients[new_phn] = new_patient
                del self.patient_dao.patients[old_phn]
                if self.autosave:
                    self.patient_dao.save_patients()
            return new_patient
        raise IllegalOperationException

    @check_login
    def delete_patient(self, phn):
        # Check if trying to delete current patient
        if self.current_patient and self.current_patient.phn == phn:
            raise IllegalOperationException
            
        if self.patient_dao.delete_patient(phn):
            return True
        raise IllegalOperationException

    @check_login
    def list_patients(self):
        return self.patient_dao.list_patients()

    @check_login
    def select_patient(self, phn):
        patient = self.search_patient(phn)
        if patient:
            self.current_patient = patient
            return True
        raise IllegalOperationException

    @check_login
    def get_current_patient(self):
        return self.current_patient
    
    @check_login
    def set_current_patient(self, phn):
        patient = self.search_patient(phn)
        if patient:
            self.current_patient = patient
            return True
        raise IllegalOperationException
    
    @check_login
    def unset_current_patient(self):
        """Unsets the current patient."""
        if self.current_patient:
            self.current_patient = None
            return True
        return False

    @check_login
    def add_note(self, text):
        if not self.current_patient:
            raise NoCurrentPatientException
        return self.current_patient.add_note(text)

    @check_login
    def list_notes(self):
        if not self.current_patient:
            raise NoCurrentPatientException
        return self.current_patient.list_notes()
    
    @check_login
    def search_note(self, note_id):
        if not self.current_patient:
            raise NoCurrentPatientException
        return self.current_patient.note_dao.search_note(note_id)
    
    @check_login
    def create_note(self, text):
        if not self.current_patient:
            raise NoCurrentPatientException
        return self.current_patient.add_note(text)
    
    @check_login
    def retrieve_notes(self, search_string):
        """Retrieves notes containing the search string."""
        if not self.current_patient:
            raise NoCurrentPatientException
        return self.current_patient.note_dao.retrieve_notes(search_string)
    
    @check_login
    def update_note(self, note_id, text):
        """Updates the text of a note with the given ID."""
        if not self.current_patient:
            raise NoCurrentPatientException
        return self.current_patient.note_dao.update_note(note_id, text)
    
    @check_login
    def delete_note(self, note_id):
        """Deletes a note with the given ID."""
        if not self.current_patient:
            raise NoCurrentPatientException
        return self.current_patient.note_dao.delete_note(note_id)