from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import  EnseignantForm, ModuleForm, FiliereForm, SalleForm, GroupeForm, SeanceForm
from .models import Filiere, Enseignant, Module, Salle, Groupe, Seance


urlpatterns = [
    
    path('', views.home, name='home'),
    path('accueil/', views.accueil, name='accueil'),
    path('login/', auth_views.LoginView.as_view(), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('acc-res/', views.enseignant_login, name='enseignant_login'),
    path('dashboard/', views.dashboard_enseignant, name='dashboard_enseignant'),
    
    
    path('emploi/', views.visualiser_emploi_du_temps, name='emploi'),
    path('export/excel/', views.exporter_excel, name='export_excel'),
    path('export/pdf/', views.exporter_pdf_enseignant, name='export_pdf'),
    path('export_pdf/<int:filiere_id>/', views.exporter_pdf, name='export_pdf'),

   
    path('generer/groupes/', views.generer_groupes, name='generer_groupes'),
    path('generer/emploi/', views.generer_emploi, name='generer_emploi'),
    path('generer/seances/', views.generer_seances_automatiquement, name='generer_seances'),

path('ajouter/filiere/', views.ajouter_filiere, name='ajouter_filiere'),
path('ajouter/enseignant/', views.ajouter_enseignant, name='ajouter_enseignant'),
path('ajouter/module/', views.ajouter_module, name='ajouter_module'),
path('ajouter/salle/', views.ajouter_salle, name='ajouter_salle'),
path('ajouter/groupe/', views.ajouter_groupe, name='ajouter_groupe'),
path('ajouter/seance/', views.ajouter_seance, name='ajouter_seance'),

path('liste/filieres/', views.liste_filieres, name='liste_filieres'),
path('liste/enseignants/', views.liste_enseignants, name='liste_enseignants'),
path('liste/modules/', views.liste_modules, name='liste_modules'),
path('liste/salles/', views.liste_salles, name='liste_salles'),
path('liste/groupes/', views.liste_groupes, name='liste_groupes'),
path('liste/seances/', views.liste_seances, name='liste_seances'),
 path('salles-libres/', views.liste_salles_disponibles, name='liste_salles_disponibles'),

path('modifier/filiere/<int:pk>/', lambda r, pk: views.modifier_entite(r, Filiere, FiliereForm, pk, 'liste_filieres'), name='modifier_filieres'),
path('supprimer/filiere/<int:pk>/', lambda r, pk: views.supprimer_entite(r, Filiere, pk, 'liste_filieres'), name='supprimer_filieres'),

path('modifier/enseignant/<int:pk>/', lambda r, pk: views.modifier_entite(r, Enseignant, EnseignantForm, pk, 'liste_enseignants'), name='modifier_enseignants'),
path('supprimer/enseignant/<int:pk>/', lambda r, pk: views.supprimer_entite(r, Enseignant, pk, 'liste_enseignants'), name='supprimer_enseignants'),

path('modifier/module/<int:pk>/', lambda r, pk: views.modifier_entite(r, Module, ModuleForm, pk, 'liste_modules'), name='modifier_modules'),
path('supprimer/module/<int:pk>/', lambda r, pk: views.supprimer_entite(r, Module, pk, 'liste_modules'), name='supprimer_modules'),

path('modifier/salle/<int:pk>/', lambda r, pk: views.modifier_entite(r, Salle, SalleForm, pk, 'liste_salles'), name='modifier_salles'),
path('supprimer/salle/<int:pk>/', lambda r, pk: views.supprimer_entite(r, Salle, pk, 'liste_salles'), name='supprimer_salles'),

path('modifier/groupe/<int:pk>/', lambda r, pk: views.modifier_entite(r, Groupe, GroupeForm, pk, 'liste_groupes'), name='modifier_groupes'),
path('supprimer/groupe/<int:pk>/', lambda r, pk: views.supprimer_entite(r, Groupe, pk, 'liste_groupes'), name='supprimer_groupes'),

path('modifier/seance/<int:pk>/', lambda r, pk: views.modifier_entite(r, Seance, SeanceForm, pk, 'liste_seances'), name='modifier_seances'),
path('supprimer/seance/<int:pk>/', lambda r, pk: views.supprimer_entite(r, Seance, pk, 'liste_seances'), name='supprimer_seances'),

path('reserver/salle/<int:salle_id>/<str:jour>/<str:heure_debut>/<str:heure_fin>/', views.reserver_salle, name='reserver_salle'),



]
