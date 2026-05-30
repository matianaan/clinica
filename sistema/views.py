from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from reportlab.pdfgen import canvas

from .models import Paciente, HistoriaClinica, Examen
from .forms import PacienteForm, HistoriaClinicaForm, ExamenForm

from .models import RecetaMedica
from .forms import RecetaMedicaForm
from django.conf import settings
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

# LOGIN
def login_view(request):
    if request.method == "POST":
        usuario = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=usuario, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "login.html", {
                "error": "Usuario o contraseña incorrectos"
            })

    return render(request, "login.html")

# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("login")


# DASHBOARD
@login_required
def dashboard(request):
    total_pacientes = Paciente.objects.count()
    total_historias = HistoriaClinica.objects.count()
    total_examenes = Examen.objects.count()

    return render(request, "dashboard.html", {
        "total_pacientes": total_pacientes,
        "total_historias": total_historias,
        "total_examenes": total_examenes
    })


# LISTA PACIENTES + BUSQUEDA
@login_required
def lista_pacientes(request):
    buscar = request.GET.get("buscar")

    if buscar:
        pacientes = Paciente.objects.filter(nombre__icontains=buscar)
    else:
        pacientes = Paciente.objects.all()

    return render(request, "pacientes/lista_pacientes.html", {
        "pacientes": pacientes
    })


# AGREGAR PACIENTE
@login_required
def agregar_paciente(request):
    form = PacienteForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("lista_pacientes")

    return render(request, "pacientes/agregar_paciente.html", {
        "form": form
    })

# EDITAR PACIENTE
@login_required
def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    form = PacienteForm(request.POST or None, instance=paciente)

    if form.is_valid():
        form.save()
        return redirect("lista_pacientes")

    return render(request, "pacientes/editar_paciente.html", {
        "form": form
    })


# ELIMINAR PACIENTE
@login_required
def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)

    if request.method == "POST":
        paciente.delete()
        return redirect("lista_pacientes")

    return render(request, "pacientes/eliminar_paciente.html", {
        "paciente": paciente
    })

# DETALLE PACIENTE (EXPEDIENTE)
@login_required
def detalle_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)

    historias = HistoriaClinica.objects.filter(paciente=paciente).order_by("-fecha_creacion")
    examenes = Examen.objects.filter(paciente=paciente).order_by("-fecha")

    return render(request, "pacientes/detalle_paciente.html", {
        "paciente": paciente,
        "historias": historias,
        "examenes": examenes
    })

# AGREGAR HISTORIA CLÍNICA 
@login_required
def agregar_historia(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    form = HistoriaClinicaForm(request.POST or None)

    if form.is_valid():
        historia = form.save(commit=False)
        historia.paciente = paciente
        historia.save()
        return redirect("detalle_paciente", id=paciente.id)

    return render(request, "pacientes/agregar_historia.html", {
        "paciente": paciente,
        "form": form
    })


# SUBIR EXAMEN
@login_required
def subir_examen(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    form = ExamenForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        examen = form.save(commit=False)
        examen.paciente = paciente
        examen.save()
        return redirect("detalle_paciente", id=paciente.id)

    return render(request, "pacientes/subir_examen.html", {
        "paciente": paciente,
        "form": form
    })


# PDF HISTORIA CLÍNICA
@login_required
def historia_pdf(request, id):
    historia = get_object_or_404(HistoriaClinica, id=id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="historia_{historia.paciente.nombre}.pdf"'

    p = canvas.Canvas(response)
    y = 800

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, y, "HISTORIA CLÍNICA")
    y -= 40

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, f"Paciente: {historia.paciente.nombre}")
    y -= 20
    p.drawString(50, y, f"Edad: {historia.paciente.edad}")
    y -= 20
    p.drawString(50, y, f"Estado civil: {historia.paciente.estado_civil}")
    y -= 20
    p.drawString(50, y, f"Ocupación: {historia.paciente.ocupacion}")
    y -= 20
    p.drawString(50, y, f"Procedencia: {historia.paciente.procedencia}")
    y -= 40

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Motivo de consulta:")
    y -= 20
    p.setFont("Helvetica", 11)
    p.drawString(60, y, str(historia.motivo_consulta)[:120])
    y -= 40

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Historia de la enfermedad:")
    y -= 20
    p.setFont("Helvetica", 11)
    p.drawString(60, y, str(historia.historia_enfermedad)[:120])
    y -= 40

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Impresión clínica:")
    y -= 20
    p.setFont("Helvetica", 11)
    p.drawString(60, y, str(historia.impresion_clinica)[:120])
    y -= 40

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Tratamiento:")
    y -= 20
    p.setFont("Helvetica", 11)
    p.drawString(60, y, str(historia.tratamiento)[:120])
    y -= 40

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Laboratorios:")
    y -= 20
    p.setFont("Helvetica", 11)
    p.drawString(60, y, str(historia.laboratorios)[:120])
    y -= 40

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, f"Próxima cita: {historia.proxima_cita}")
    y -= 40

    p.setFont("Helvetica", 10)
    p.drawString(50, y, f"Fecha de creación: {historia.fecha_creacion}")

    p.showPage()
    p.save()




@login_required
def crear_receta(request, historia_id):
    historia = get_object_or_404(HistoriaClinica, id=historia_id)

    if request.method == "POST":
        form = RecetaMedicaForm(request.POST)

        if form.is_valid():
            receta = form.save(commit=False)
            receta.historia = historia
            receta.save()
            return redirect("detalle_paciente", id=historia.paciente.id)
    else:
        form = RecetaMedicaForm()

    return render(request, "pacientes/crear_receta.html", {
        "historia": historia,
        "paciente": historia.paciente,
        "form": form
    })


@login_required
def receta_pdf(request, receta_id):
    receta = get_object_or_404(RecetaMedica, id=receta_id)
    paciente = receta.historia.paciente

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="receta_{paciente.nombre}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    y = height - 50

    # LOGO
    logo_path = os.path.join(settings.BASE_DIR, "static", "img", "logo_ginefem.jpg")
    if os.path.exists(logo_path):
        p.drawImage(ImageReader(logo_path), 50, y - 80, width=90, height=70)

    # ENCABEZADO CLINICA
    p.setFont("Helvetica-Bold", 16)
    p.drawString(160, y - 20, "GineFem")

    p.setFont("Helvetica", 10)
    p.drawString(160, y - 40, "Mataquescuintla, Jalapa")
    p.drawString(160, y - 55, "Tel. Citas: 7776 9411")
    p.drawString(160, y - 70, "Correo: clinicaintegral.ginefem@gmail.com")

    y -= 110

    # DATOS DOCTORA
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, "Dra. Nancy Ruano")
    y -= 15
    p.setFont("Helvetica", 10)
    p.drawString(50, y, "Ginecología y Obstetricia")
    y -= 15
    p.drawString(50, y, "Emergencias: 5588 2595")

    y -= 30

    # DATOS PACIENTE
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, f"Paciente: {paciente.nombre}")
    y -= 15
    p.setFont("Helvetica", 10)
    p.drawString(50, y, f"Edad: {paciente.edad}")
    y -= 15
    p.drawString(50, y, f"Fecha: {receta.fecha}")

    y -= 30

    # DIAGNOSTICO
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, "Diagnóstico:")
    y -= 15
    p.setFont("Helvetica", 10)
    p.drawString(60, y, (receta.diagnostico or "")[:120])

    y -= 30

    # TRATAMIENTO
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, "Tratamiento / Medicamentos:")
    y -= 15
    p.setFont("Helvetica", 10)
    p.drawString(60, y, (receta.tratamiento or "")[:200])

    y -= 50

    # NOTA
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, "Nota:")
    y -= 15
    p.setFont("Helvetica", 10)
    p.drawString(60, y, (receta.nota or "")[:200])

    y -= 80

    # FIRMA
    p.setFont("Helvetica", 10)
    p.drawString(50, y, "______________________________")
    y -= 15
    p.drawString(50, y, "Firma y sello")

    p.showPage()
    p.save()

    return response
