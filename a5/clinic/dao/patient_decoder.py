import json
from clinic.patient import Patient

class PatientDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        self.autosave = kwargs.pop('autosave', False)
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
    
    def object_hook(self, dct):
        if isinstance(dct, list):
            #handle list of patients
            return [self.create_patient(p) for p in dct]
        elif all(k in dct for k in ('phn', 'name', 'birth_date', 'phone', 'email', 'address')):
            return self.create_patient(dct)
        return dct

    def create_patient(self, data):
        #ensure PHN is an integer
        phn = int(data['phn']) if isinstance(data['phn'], str) else data['phn']
        return Patient(
            phn,
            data['name'],
            data['birth_date'],
            data['phone'],
            data['email'],
            data['address'],
            autosave=self.autosave
        )

    def decode(self, json_str):
        data = super().decode(json_str)
        if isinstance(data, list):
            #sort patients by PHN when decoding
            return sorted(data, key=lambda x: x.phn)
        return data