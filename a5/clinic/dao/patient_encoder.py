import json
from clinic.patient import Patient

class PatientEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Patient):
            return {
                'phn': obj.phn,
                'name': obj.name,
                'birth_date': obj.birth_date,
                'phone': obj.phone,
                'email': obj.email,
                'address': obj.address
            }
        return super().default(obj)