# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm, AppointmentForm, DoctorForm, PatientForm, MedicineForm, PrescriptionForm
from .models import Appointment, Patient, Doctor, Medicine, Prescription
from django.http import HttpResponse
from .models import Appointment
from django.utils.timezone import now

@login_required
def dashboard(request):
    total_appointments = Appointment.objects.count()
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    upcoming_appointments = Appointment.objects.filter(appointment_date__gte=now()).order_by('appointment_date')[:5]

    context = {
        'total_appointments': total_appointments,
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'upcoming_appointments': upcoming_appointments,
    }
    return render(request, 'dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('dashboard')  # Redirect to dashboard
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def custom_logout(request):
    """Logs out the user and redirects to the login page."""
    if request.method == "POST":
        logout(request)
        return redirect('login')  # Redirect to the login page
    else:
        return redirect('dashboard')  # Redirect back to the dashboard if not a POST request

# List Appointments
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

# Create Appointment
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/appointment_form.html', {'form': form})

# Update Appointment
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/appointment_form.html', {'form': form})

# Delete Appointment
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})

# Generate Receipt
def appointment_receipt(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/appointment_receipt.html', {'appointment': appointment})


# List Doctors
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})

# Create Doctor
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'doctors/doctor_form.html', {'form': form})

# Update Doctor
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctors/doctor_form.html', {'form': form})

# Delete Doctor
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('doctor_list')
    return render(request, 'doctors/doctor_confirm_delete.html', {'doctor': doctor})

# List Patients
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients})

# Create Patient
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'patients/patient_form.html', {'form': form})

# Update Patient
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_form.html', {'form': form})

# Delete Patient
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})


# List Medicines
def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicines/medicine_list.html', {'medicines': medicines})

# Create Medicine
def medicine_create(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'medicines/medicine_form.html', {'form': form})

# Update Medicine
def medicine_update(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'medicines/medicine_form.html', {'form': form})

# Delete Medicine
def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        medicine.delete()
        return redirect('medicine_list')
    return render(request, 'medicines/medicine_confirm_delete.html', {'medicine': medicine})

# List Prescriptions
def prescription_list(request):
    prescriptions = Prescription.objects.all()
    return render(request, 'prescriptions/prescription_list.html', {'prescriptions': prescriptions})

# Create Prescription
def prescription_create(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.save()
            form.save_m2m()  # Save the ManyToMany relationship
            return redirect('prescription_list')
    else:
        form = PrescriptionForm()
    return render(request, 'prescriptions/prescription_form.html', {'form': form})

# Update Prescription
def prescription_update(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect('prescription_list')
    else:
        form = PrescriptionForm(instance=prescription)
    return render(request, 'prescriptions/prescription_form.html', {'form': form})

# Delete Prescription
def prescription_delete(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if request.method == 'POST':
        prescription.delete()
        return redirect('prescription_list')
    return render(request, 'prescriptions/prescription_confirm_delete.html', {'prescription': prescription})


def prescription_receipt(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    return render(request, 'prescriptions/prescription_receipt.html', {'prescription': prescription})
