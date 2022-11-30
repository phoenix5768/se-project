from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . models import Patient, Doctor, Specialization, Appointment, Preappointment
from django.contrib.auth.decorators import login_required
from .forms import PatientForm, DoctorForm, AppointmentForm



def home(request):
    return render(request, "authentication/index.html")


@login_required
def adminpage(request):
    
    patients = Patient.objects.all()
    #patients_list = {'patients': patients}


    doctors = Doctor.objects.all()
    #doctors_list = {'doctors': doctors}

    return render(request, "authentication/adminpage.html", {'patients': patients, 'doctors': doctors})


def update_patient(request, patient_id):
    patient = Patient.objects.get(id_number = patient_id)
    
    form = PatientForm(request.POST or None, instance = patient)

    if form.is_valid():
        form.save()
        return redirect('adminpage')
    return render(request, "authentication/update_patient.html", {'patient': patient, 'form': form})


def delete_patient(request, patient_id):
    patient = Patient.objects.get(id_number = patient_id)
    patient.delete()

    return redirect('adminpage')


@login_required
def patient(request):
    """
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        mname = request.POST['mname']
        iin = request.POST['iin']
        dob = request.POST['dob']
        blood = request.POST['blood']
        emergency = request.POST['emergency']
        num = request.POST['num']
        email = request.POST['email']
        address = request.POST['address']
        martial = request.POST['martial']


        if Patient.objects.filter(iin_number = iin):
            messages.error(request, "Patient alreaedy exists!")
            return redirect('patient')
        
        if Patient.objects.filter(email = email):
            messages.error(request, "Email already exists!")
            return redirect('patient')
        

        mypatient = Patient.objects.create(fname = fname, lname = lname, mname = mname, iin_number = iin, date_of_birth = dob,
                                            blood_group = blood, emergency_contact_number = emergency, contact_number = num,
                                            email = email, address = address, martial_status = martial)
        
        mypatient.save()

        messages.success(request, "The patient has been successfully registered.")


        return redirect('adminpage')

    return render(request, "authentication/patient.html")
    """
    submitted = False
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('adminpage')
        
        else:
            form = PatientForm
            if 'submitted' in request.GET:
                submitted = True

    form = PatientForm
    return render(request, "authentication/patient.html", {'form': form, 'submitted': submitted})


def update_doctor(request, doctor_id):
    doctor = Doctor.objects.get(id_number = doctor_id)
    
    form = DoctorForm(request.POST or None, instance = doctor)

    if form.is_valid():
        form.save()
        return redirect('adminpage')
    return render(request, "authentication/update_doctor.html", {'doctor': doctor, 'form': form})


def delete_doctor(request, doctor_id):
    doctor = Doctor.objects.get(id_number = doctor_id)
    doctor.delete()

    return redirect('adminpage')


@login_required
def doctor(request):
    """"
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        mname = request.POST['mname']
        iin = request.POST['iin']
        dob = request.POST['dob']
        num = request.POST['num']
        department = request.POST['department']
        specialization = request.POST['specialization']
        experience = request.POST['experience']
        category = request.POST['category']
        price = request.POST['price']
        schedule = request.POST['schedule']
        degree = request.POST['degree']
        rating = request.POST['rating']
        address = request.POST['address']
        dict = {'doctor': doctor, date, time}

        if Doctor.objects.filter(iin_number = iin):
            messages.error(request, "Doctor alreaedy exists!")
            return redirect('doctor')


        mydoctor = Doctor.objects.create(fname = fname, lname = lname, mname = mname, iin_number = iin, date_of_birth = dob,
                                            contact_number = num, department_id = department, specialization_details_id = specialization,
                                            experience = experience, category = category, price = price, schedule_details = schedule,
                                            education = degree, rating = rating, address = address,)
        
        mydoctor.save()

        messages.success(request, "The doctor has been successfully registered.")


        return redirect('adminpage')



    return render(request, "authentication/doctor.html")
    """
    submitted = False
    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('adminpage')
        
        else:
            form = DoctorForm
            if 'submitted' in request.GET:
                submitted = True

    form = DoctorForm
    return render(request, "authentication/doctor.html", {'form': form, 'submitted': submitted})


def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)

        if user is not None: 
            login(request, user)
            #fname = user.first_name
            messages.success(request, f' welcome {username}!! ')
            return redirect('home')
        
        else:
            messages.info(request, 'account does not exists')
            return HttpResponseRedirect('signin')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')


def make_appointment(request):
    doctors = Doctor.objects.filter()
    '''
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('make-appointment')

        else:
            form = AppointmentForm

    form = AppointmentForm'''

    if request.method == "POST":
        doc = request.POST["doctor"]
        doctor = Doctor.objects.get(id_number = doc)
        date = request.POST["date"]
        timeslot = request.POST["timeslot"]
        patient_name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]

        if Appointment.objects.filter(doctor=doctor, date=date, timeslot=timeslot):
            messages.error(request, "Timeslot is not available")
            return redirect('make-appointment')
        else:
            myappointment = Preappointment.objects.create(doctor_id=doc, date=date, timeslot=timeslot,
                                                       patient_name=patient_name, phone=phone, email=email)
            myappointment.save()
            messages.success(request, "Your appointment has been send to the administrator. You will receive your confirmation very soon!")


    context = {
        'doctors': doctors
    }

    return render(request, "authentication/make_appointment.html", context)

def confirm_appointment(request):
    appointments = Preappointment.objects.filter()
    doctors = Doctor.objects.filter()
    context = {
        'appointments': appointments,
        'doctors': doctors,
    }
    return render(request, "authentication/confirm_appointment.html", context)

def appointment(request):
    return render(request, "authentication/appointment.html")

def specialization(request):
    doctors = Doctor.objects.filter()
    specializations = Specialization.objects.filter()
    appointments = Appointment.objects.filter()

    context = {
        'doctors': doctors,
        'specializations': specializations,
        'appointments': appointments,
    }
    return render(request, "authentication/specialization.html", context)

def delete_preappointment(request, doctor_id, date, timeslot):
    preappointment = Preappointment.objects.get(doctor_id=doctor_id, date=date, timeslot=timeslot)
    preappointment.delete()

    return redirect('confirm-appointment')

def confirm_request(request, doctor_id, date, timeslot):
    doctors = Doctor.objects.get(id_number=doctor_id)
    appointments = Preappointment.objects.get(doctor_id=doctor_id, date=date, timeslot=timeslot)
    if request.method == "POST":
        doc = appointments.doctor_id
        doctor = Doctor.objects.get(id_number = doc)
        date = appointments.date
        timeslot = appointments.timeslot
        patient_name = appointments.patient_name
        phone = appointments.phone
        email = appointments.email

        if Appointment.objects.filter(doctor=doctor, date=date, timeslot=timeslot):
            messages.error(request, "Timeslot is not available")
            return redirect('make-appointment')
        else:
            myappointment = Appointment.objects.create(doctor=doctor, date=date, timeslot=timeslot,
                                                       patient_name=patient_name, phone=phone, email=email)
            myappointment.save()
            preappointment = Preappointment.objects.get(doctor_id=doctor_id, date=date, timeslot=timeslot)
            preappointment.delete()
            messages.success(request, "Appointment was set successfully")


    context = {
        'doctors': doctors,
        'appointments': appointments
    }


    return render(request, "authentication/confirm_request.html", context)