from django import forms
from django.forms import ModelForm
from .models import Patient, Doctor, Appointment


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ('date_of_birth', 'iin_number', 'id_number', 'fname', 'mname', 'lname', 'blood_group', 'emergency_contact_number', 'contact_number', 'email', 'address', 'martial_status')
        

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ("__all__")


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ('doctor', 'date', 'timeslot')