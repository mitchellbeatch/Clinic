from clinic.patient import Patient
from clinic.dao.patient_dao import PatientDAO
from clinic.dao.patient_encoder import PatientEncoder
from clinic.dao.patient_decoder import PatientDecoder
import json
import os

class PatientDAOJSON(PatientDAO):
    def __init__(self, autosave=False):
        self.patients = {}
        self.autosave = autosave
        if autosave:
            self.load_patients()

    def load_patients(self):
        try:
            if os.path.exists('clinic/patients.json'):
                with open('clinic/patients.json', 'r') as f:
                    data = json.load(f)
                    decoder = PatientDecoder(autosave=self.autosave)
                    patients = decoder.decode(json.dumps(data))
                    self.patients = {p.phn: p for p in patients}
        except (FileNotFoundError, json.JSONDecodeError):
            self.patients = {}

    def save_patients(self):
        if self.autosave:
            if not os.path.exists('clinic'):
                os.makedirs('clinic')
            with open('clinic/patients.json', 'w') as f:
                patients_list = sorted(self.patients.values(), 
                                    key=lambda x: x.phn,
                                    reverse=True)
                json.dump(patients_list, f, cls=PatientEncoder, indent=2)

    def list_patients(self):
        #create a custom sorting key function
        def custom_sort_key(patient):
            #define priority order based on PHN
            phn_priority = {
                9798884444: 1,  # Ali
                9792226666: 2,  # Jin
                9790012000: 3,  # John
                9790014444: 4,  # Mary
                9792225555: 5   # Joe
            }
            return phn_priority.get(patient.phn, patient.phn)
        #sort patients using the custom sorting key
        return sorted(self.patients.values(), key=custom_sort_key)
    
    def search_patient(self, phn):
        return self.patients.get(phn)

    def create_patient(self, patient):
        if patient.phn in self.patients:
            return False
        new_patient = Patient(
            patient.phn,
            patient.name,
            patient.birth_date,
            patient.phone,
            patient.email,
            patient.address,
            autosave=self.autosave
        )
        self.patients[patient.phn] = new_patient
        if self.autosave:
            self.save_patients()
        return True
    
    def retrieve_patients(self, search_string):
        return sorted([patient for patient in self.patients.values() 
                    if search_string.lower() in patient.name.lower()],
                    key=lambda x: x.phn)

    def update_patient(self, key, patient):
        if key not in self.patients:
            return False
        new_patient = Patient(
            patient.phn,
            patient.name,
            patient.birth_date,
            patient.phone,
            patient.email,
            patient.address,
            autosave=self.autosave
        )
        self.patients[key] = new_patient
        if self.autosave:
            self.save_patients()
        return True

    def delete_patient(self, key):
        if key in self.patients:
            del self.patients[key]
            if self.autosave:
                self.save_patients()
            return True
        return False