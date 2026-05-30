from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('pacientes/', views.lista_pacientes, name="lista_pacientes"),
    path('pacientes/agregar/', views.agregar_paciente, name="agregar_paciente"),
    path('pacientes/editar/<int:id>/', views.editar_paciente, name="editar_paciente"),
    path('pacientes/eliminar/<int:id>/', views.eliminar_paciente, name="eliminar_paciente"),

    # EXPEDIENTE
    path("paciente/<int:id>/", views.detalle_paciente, name="detalle_paciente"),
    path("paciente/<int:id>/historia/nueva/", views.agregar_historia, name="agregar_historia"),

    # PDF HISTORIA CLINICA
    path("historia/<int:id>/pdf/", views.historia_pdf, name="historia_pdf"),

    # SUBIR EXAMEN
    path("paciente/<int:id>/examen/nuevo/", views.subir_examen, name="subir_examen"),

    # RECETAS
    path("historia/<int:historia_id>/receta/nueva/", views.crear_receta, name="crear_receta"),
    path("receta/<int:receta_id>/pdf/", views.receta_pdf, name="receta_pdf"),
]