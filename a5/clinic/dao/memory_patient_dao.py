from clinic.dao.patient_dao import PatientDAO

class MemoryPatientDAO(PatientDAO):
    def __init__(self):
        self.patients = {} 

    def search_patient(self, key):
        return self.patients.get(key)
    
    def create_patient(self, patient):
        if patient.phn in self.patients:
            return False
        self.patients[patient.phn] = patient
        return True
    
    def retrieve_patients(self, search_string):
        return [patient for patient in self.patients.values() if 
                search_string.lower() in patient.name.lower()]
    
    def update_patient(self, key, patient):
        if key not in self.patients:
            return False
        self.patients[key] = patient
        return True
    
    def delete_patient(self, key):
        if key in self.patients:
            del self.patients[key]
            return True
        return False
    
    def list_patients(self):
        return list(self.patients.values())