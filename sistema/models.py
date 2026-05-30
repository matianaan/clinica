from django.db import models


class Paciente(models.Model):
    nombre = models.CharField(max_length=200)
    edad = models.IntegerField()
    estado_civil = models.CharField(max_length=100)
    religion = models.CharField(max_length=100, blank=True, null=True)
    ocupacion = models.CharField(max_length=150)
    procedencia = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre


class HistoriaClinica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

    motivo_consulta = models.TextField()
    historia_enfermedad = models.TextField()

    # Antecedentes
    medicos = models.TextField(blank=True, null=True)
    quirurgicos = models.TextField(blank=True, null=True)
    alergicos = models.TextField(blank=True, null=True)
    traumaticos = models.TextField(blank=True, null=True)

    # Ginecoobstétricos
    g = models.CharField(max_length=10, blank=True, null=True)
    p = models.CharField(max_length=10, blank=True, null=True)
    c = models.CharField(max_length=10, blank=True, null=True)
    a = models.CharField(max_length=10, blank=True, null=True)
    hv = models.CharField(max_length=10, blank=True, null=True)
    hm = models.CharField(max_length=10, blank=True, null=True)

    menarquia = models.CharField(max_length=50, blank=True, null=True)
    coitarquia = models.CharField(max_length=50, blank=True, null=True)
    no_parejas = models.IntegerField(blank=True, null=True)
    fur = models.DateField(blank=True, null=True)
    ciclos_menstruales = models.CharField(max_length=100, blank=True, null=True)
    planificacion_familiar = models.CharField(max_length=150, blank=True, null=True)

    # Examen físico
    pa = models.CharField(max_length=50, blank=True, null=True)
    fc = models.CharField(max_length=50, blank=True, null=True)
    fr = models.CharField(max_length=50, blank=True, null=True)
    temperatura = models.CharField(max_length=50, blank=True, null=True)
    so2 = models.CharField(max_length=50, blank=True, null=True)
    peso = models.CharField(max_length=50, blank=True, null=True)
    talla = models.CharField(max_length=50, blank=True, null=True)
    imc = models.CharField(max_length=50, blank=True, null=True)

    impresion_clinica = models.TextField(blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    laboratorios = models.TextField(blank=True, null=True)
    proxima_cita = models.DateField(blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Historia de {self.paciente.nombre}"


class Examen(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to="examenes/")
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Examen de {self.paciente.nombre}"
    
class RecetaMedica(models.Model):
    historia = models.ForeignKey("HistoriaClinica", on_delete=models.CASCADE, related_name="recetas")

    fecha = models.DateField(auto_now_add=True)

    diagnostico = models.TextField(blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    nota = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Receta - {self.historia.paciente.nombre} - {self.fecha}" 


# ✅ NUEVO MODELO: RECETA MÉDICA
class RecetaMedica(models.Model):
    historia = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, related_name="recetas")

    fecha = models.DateField(auto_now_add=True)

    diagnostico = models.TextField(blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    nota = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Receta - {self.historia.paciente.nombre} - {self.fecha}" 