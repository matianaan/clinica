from django import forms
from .models import Paciente, HistoriaClinica, Examen, RecetaMedica


# FORMULARIO PACIENTE
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            "nombre",
            "edad",
            "estado_civil",
            "religion",
            "ocupacion",
            "procedencia",
            "telefono",
        ]


# FORMULARIO HISTORIA CLÍNICA
class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        exclude = ["paciente", "fecha_creacion"]

        widgets = {
            "motivo_consulta": forms.Textarea(attrs={"rows": 3}),
            "historia_enfermedad": forms.Textarea(attrs={"rows": 4}),

            "medicos": forms.Textarea(attrs={"rows": 2}),
            "quirurgicos": forms.Textarea(attrs={"rows": 2}),
            "alergicos": forms.Textarea(attrs={"rows": 2}),
            "traumaticos": forms.Textarea(attrs={"rows": 2}),

            "impresion_clinica": forms.Textarea(attrs={"rows": 3}),
            "tratamiento": forms.Textarea(attrs={"rows": 3}),
            "laboratorios": forms.Textarea(attrs={"rows": 3}),

            "pa": forms.TextInput(attrs={"placeholder": "Ej: 120/80"}),
            "fc": forms.TextInput(attrs={"placeholder": "Ej: 80 bpm"}),
            "fr": forms.TextInput(attrs={"placeholder": "Ej: 18 rpm"}),
            "temperatura": forms.TextInput(attrs={"placeholder": "Ej: 36.5°C"}),
            "so2": forms.TextInput(attrs={"placeholder": "Ej: 98%"}),
            "peso": forms.TextInput(attrs={"placeholder": "kg"}),
            "talla": forms.TextInput(attrs={"placeholder": "m"}),
            "imc": forms.TextInput(attrs={"placeholder": "IMC"}),
        }


# FORMULARIO EXÁMENES
class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ["archivo", "descripcion"]


# FORMULARIO RECETA MÉDICA
class RecetaMedicaForm(forms.ModelForm):
    class Meta:
        model = RecetaMedica
        fields = ["diagnostico", "tratamiento", "nota"]

        widgets = {
            "diagnostico": forms.Textarea(attrs={"rows": 3}),
            "tratamiento": forms.Textarea(attrs={"rows": 4}),
            "nota": forms.Textarea(attrs={"rows": 3}),
        }