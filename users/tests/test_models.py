class TestPatient:
    def test_model(self, patient, surgeon):
        assert patient.user.email == "am.naimi@gmail.com"
        assert patient.user.first_name == "Amir"
        assert patient.user.last_name == "Naeimi"

        assert surgeon.user.email == "am.naimi@gmail.com"
        assert surgeon.user.first_name == "Parisa"
        assert surgeon.user.last_name == "Rahbari"
