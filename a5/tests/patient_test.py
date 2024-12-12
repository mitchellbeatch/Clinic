import unittest
from clinic.controller import Controller
from clinic.patient import Patient

class TestController(unittest.TestCase):
    def setUp(self):
        """Initialize a Controller instance before each test"""
        self.controller = Controller(users={"user": "clinic2024"})
        """Initialize Patients"""
        patient_1 = Patient(123, "Tim", "1985-01-10", 2228953, "tim@email.com", "2041 Cedar Ave")
        patient_1a = Patient(123, "Tim", "1985-01-10", 2228953, "tim@email.com", "2041 Cedar Ave") 
        patient_2 = Patient(297, "Andy", "1994-09-03", 5879265, "andy@email.com", "391 Burgundy Street")
        patient_3 = Patient(314, "Julia", "2000-12-05", 8955732, "julia@email.com", "752 Scott Street")

    def test_create_patient(self):
        patient_1 = Patient(123, "Tim", "1985-01-10", 2228953, "tim@email.com", "2041 Cedar Ave")
        patient_1a = Patient(123, "Tim", "1985-01-10", 2228953, "tim@email.com", "2041 Cedar Ave") 
        patient_2 = Patient(297, "Andy", "1994-09-03", 5879265, "andy@email.com", "391 Burgundy Street")
        patient_3 = Patient(314, "Julia", "2000-12-05", 8955732, "julia@email.com", "752 Scott Street")
        # Ensure patients cannot be created without login
        self.assertIsNone(self.controller.create_patient(123, "Tim", "1985-01-10", 2228953, "tim@email.com", "2041 Cedar Ave"))

        # Log in the user
        self.assertTrue(self.controller.login("user", "clinic2024"), "login correctly")

        # Create a new patient
        self.assertEqual(self.controller.create_patient(123, "Tim", "1985-01-10", 2228953, "tim@email.com", "2041 Cedar Ave"), 
                         patient_1, "Patient created succesfully")
        # Ensure patients cannot be overwritten
        self.assertIsNone(self.controller.create_patient(123, "Tim", "1985-01-10", 2228953, "tim@email.com", "2041 Cedar Ave"), 
                          "Patient not overwritten")

    def test_retrieve_patients(self):
        # patients for comparison
        expected_patient_1 = Patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")
        expected_patient_2 = Patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
        expected_patient_3 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        expected_patient_4 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        expected_patient_5 = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

        # must be logged in
        self.assertIsNone(self.controller.retrieve_patients("John Doe"), "cannot retrieve patients without logging in")

        # login and create patients
        self.assertTrue(self.controller.login("user", "clinic2024"), "login correctly")
        self.controller.create_patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")
        self.controller.create_patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
        self.controller.create_patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        self.controller.create_patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

        # retrieve one patient
        retrieved_list = self.controller.retrieve_patients("Mary Doe")
        self.assertEqual(len(retrieved_list), 1, "retrieved list of patients has size 1")
        actual_patient = retrieved_list[0]
        self.assertEqual(actual_patient, expected_patient_4, "retrieved patient in the list is Mary Doe")

        # retrieve zero patients
        retrieved_list = self.controller.retrieve_patients("Smith")
        self.assertEqual(len(retrieved_list), 0)

    def test_update_patient(self):
        # some patients that may be updated
        expected_patient_1 = Patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")
        expected_patient_2 = Patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
        expected_patient_3 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        expected_patient_4 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        expected_patient_5 = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

        # cannot do operation without logging in
        self.assertFalse(self.controller.update_patient(9790012000, 9790012000, "John Doe", "2000-10-10", "278 999 4041", "john.doe@hotmail.com", "205 Foul Bay Rd, Oak Bay"), 
            "cannot update patient without logging in")

        # login
        self.assertTrue(self.controller.login("user", "clinic2024"), "login correctly")

        # try to update a patient when there are no patients in the system
        self.assertFalse(self.controller.update_patient(9790012000, 9790012000, "John Doe", "2000-10-10", "278 999 4041", "john.doe@hotmail.com", "205 Foul Bay Rd, Oak Bay"),
            "cannot update patient when there are no patients in the system")

        # create some patients
        self.controller.create_patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")
        self.controller.create_patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
        self.controller.create_patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        self.controller.create_patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

        # update one patient, but keep the Patient key (personal health number) unchanged
        self.assertTrue(self.controller.update_patient(9790012000, 9790012000, "John Doe", "2000-10-10", "278 999 4041", "john.doe@hotmail.com", "205 Foul Bay Rd, Oak Bay"), 
            "update patient data and keep the PHN unchanged")
        actual_patient = self.controller.search_patient(9790012000)
        self.assertNotEqual(actual_patient, expected_patient_3, "patient has updated data, cannot be equal to the original data")
        expected_patient_3a = Patient(9790012000, "John Doe", "2000-10-10", "278 999 4041", "john.doe@hotmail.com", "205 Foul Bay Rd, Oak Bay")
        self.assertEqual(actual_patient, expected_patient_3a, "patient was updated, their data has to be updated and correct")

        # update one patient, and change the Patient key (personal health number) as well
        self.assertTrue(self.controller.update_patient(9792225555, 9793334444, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@gmail.com", "200 Quadra St, Victoria"), 
            "update patient data and also change the PHN")
        actual_patient = self.controller.search_patient(9793334444)
        self.assertNotEqual(actual_patient, expected_patient_5, "patient has updated data, cannot be equal to the original data")
        expected_patient_5a = Patient(9793334444, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@gmail.com", "200 Quadra St, Victoria")
        self.assertEqual(actual_patient, expected_patient_5a, "patient was updated, their data has to be updated and correct")

        # update one patient with a conflicting existing personal health number
        self.assertFalse(self.controller.update_patient(9790014444, 9798884444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria"), 
            "cannot update patient and give them a registered phn")


    def test_delete_patient(self):
        # some patients that may be deleted
        expected_patient_1 = Patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")
        expected_patient_2 = Patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
        expected_patient_3 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        expected_patient_4 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        expected_patient_5 = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

        # cannot do operation without logging in
        self.assertFalse(self.controller.delete_patient(9798884444), "cannot delete patient without logging in")

        # login
        self.assertTrue(self.controller.login("user", "clinic2024"), "login correctly")

        # try to delete a patient when there are no patients in the system
        self.assertFalse(self.controller.delete_patient(9790012000), "cannot delete patient when there are no patients in the system")

        # add some patients
        self.controller.create_patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")
        self.controller.create_patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
        self.controller.create_patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        self.controller.create_patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

        # delete one patient at the start of the collection
        self.assertTrue(self.controller.delete_patient(9798884444), "delete patient from the start of the collection")
        self.assertIsNone(self.controller.search_patient(9798884444), "deleted patient cannot be found in the system")

        # delete one patient at the middle of the collection
        self.assertTrue(self.controller.delete_patient(9790012000), "delete patient from the middle of the collection")
        self.assertIsNone(self.controller.search_patient(9790012000), "deleted patient cannot be found in the system")

        # delete one patient at the end of the collection
        self.assertTrue(self.controller.delete_patient(9792225555), "delete patient from the end of the collection")
        self.assertIsNone(self.controller.search_patient(9792225555), "deleted patient cannot be found in the system")


    def test_list_patients(self):
        # some patients that may be listed
        expected_patient_1 = Patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")
        expected_patient_2 = Patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
        expected_patient_3 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        expected_patient_4 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        expected_patient_5 = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

        # cannot do operation without logging in
        self.assertIsNone(self.controller.list_patients(), "cannot list patients without logging in")

        # login
        self.assertTrue(self.controller.login("user", "clinic2024"), "login correctly")

        # listing patients when there are no patients in the system
        patients_list = self.controller.list_patients()
        self.assertEqual(len(patients_list), 0, "list of patients has size 0")

        # add one patient
        self.controller.create_patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")

        # listing patients in a singleton list
        patients_list = self.controller.list_patients()
        self.assertEqual(len(patients_list), 1, "list of patients has size 1")
        self.assertEqual(patients_list[0], expected_patient_1, "patient Ali Mesbah is the only one in the list of patients")

        # add some more patients
        self.controller.create_patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
        self.controller.create_patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        self.controller.create_patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        self.controller.create_patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

        # listing patients in a larger list
        patients_list = self.controller.list_patients()
        self.assertEqual(len(patients_list), 5, "list of patients has size 5")
        self.assertEqual(patients_list[0], expected_patient_1, "patient 1 is the first in the list of patients")
        self.assertEqual(patients_list[1], expected_patient_2, "patient 2 is the second in the list of patients")
        self.assertEqual(patients_list[2], expected_patient_3, "patient 3 is the third in the list of patients")
        self.assertEqual(patients_list[3], expected_patient_4, "patient 4 is the fourth in the list of patients")
        self.assertEqual(patients_list[4], expected_patient_5, "patient 5 is the fifth in the list of patients")

        # deleting some patients
        self.controller.delete_patient(9790012000)
        self.controller.delete_patient(9798884444)
        self.controller.delete_patient(9792225555)

        # listing patients after deleting some patients
        patients_list = self.controller.list_patients()
        self.assertEqual(len(patients_list), 2, "list of patients has size 2")
        self.assertEqual(patients_list[0], expected_patient_2, "patient 2 is the first in the list of patients")
        self.assertEqual(patients_list[1], expected_patient_4, "patient 4 is the second in the list of patients")

if __name__ == "__main__":
    unittest.main()
