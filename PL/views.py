from django.shortcuts import render, redirect
from .models import *
from .models import DisponibiliteEnseignant, DisponibiliteSalle
from .forms import DisponibiliteEnseignantForm, DisponibiliteSalleForm
from .forms import  EnseignantForm, ModuleForm, FiliereForm, SalleForm, GroupeForm, SeanceForm
from django.http import HttpResponse
import datetime
import pandas as pd
from reportlab.pdfgen import canvas
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Count
from datetime import datetime, timedelta, time
from django.db.models import Q
from ortools.sat.python import cp_model
def accueil(request):
    return render(request, 'accueil.html')


# def visualiser_emploi_du_temps(request):
#      seances = Seance.objects.all().select_related('module', 'groupe__filiere', 'salle', 'enseignant')
#      filieres = Filiere.objects.all()
#      return render(request, 'emploi.html', {'seances': seances, 'filieres': filieres})

def visualiser_emploi_du_temps(request):
    # Récupération des données
    seances = Seance.objects.all().select_related('module', 'groupe__filiere', 'salle', 'enseignant')
    filieres = Filiere.objects.all()
    
    # Structure des créneaux horaires
    creneaux = [
        ('08:30', '10:30'),
        ('10:45', '12:45'),
        ('14:00', '16:00'),
        ('16:15', '18:15')
    ]
    
    # Jours de la semaine
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
    
    return render(request, 'emploi.html', {
        'seances': seances,
        'filieres': filieres,
        'creneaux': creneaux,
        'jours': jours
    })

def exporter_excel(request):
    seances = Seance.objects.all()
    data = [{
        'Module': s.module.nom,
        'Salle': s.salle.nom,
        'Groupe': s.groupe.nom,
        'Jour': s.jour,
        'Heure début': s.heure_debut,
        'Heure fin': s.heure_fin
    } for s in seances]
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="emploi_du_temps.xlsx"'
    df.to_excel(response, index=False)
    return response


def ajouter_filiere(request):
    form = FiliereForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('accueil')
    return render(request, 'form.html', {'form': form})

def ajouter_enseignant(request):
    form = EnseignantForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('accueil')
    return render(request, 'form.html', {'form': form})

def ajouter_module(request):
    form = ModuleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('accueil')
    return render(request, 'form.html', {'form': form})

def ajouter_salle(request):
    form = SalleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('accueil')
    return render(request, 'form.html', {'form': form})

def ajouter_groupe(request):
    form = GroupeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('accueil')
    return render(request, 'form.html', {'form': form})

def ajouter_seance(request):
    if request.method == 'POST':
        form = SeanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_seances')
    else:
        form = SeanceForm()
    return render(request, 'form.html', {'form': form, 'titre': 'Ajouter une séance'})



def generer_seances_automatiquement(request):
    for module in Module.objects.all():
        for filiere in Filiere.objects.all():
            for type_seance in ['CM', 'TD', 'TP']:
                for groupe in Groupe.objects.filter(filiere=filiere):
                    heure_debut = datetime.combine(datetime.today(), time(8, 0))  
                    heure_fin = heure_debut + timedelta(hours=2)

                    seance = Seance(
                        module=module,
                        type_seance=type_seance,
                        filiere=filiere,
                        groupe=groupe,
                        jour="Lundi",  
                        heure_debut=heure_debut.time(),  
                        heure_fin=heure_fin.time(),  
                    )
                    seance.save()

    return render(request, 'liste.html', {'message': 'Séances générées avec succès!'})



def exporter_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="emploi_du_temps.pdf"'
    p = canvas.Canvas(response)
    seances = Seance.objects.all()
    y = 800
    for s in seances:
        p.drawString(100, y, f"{s.jour} - {s.heure_debut} à {s.heure_fin} : {s.module.nom} en {s.salle.nom} (Groupe {s.groupe.nom})")
        y -= 20
    p.showPage()
    p.save()
    return response


# def exporter_pdf(request):
#     # Configuration du PDF
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="emploi_du_temps.pdf"'
    
#     # Création du document en format paysage
#     doc = SimpleDocTemplate(response, pagesize=landscape(A4))
#     elements = []
    
#     # Styles
#     styles = getSampleStyleSheet()
#     style_title = styles['Title']
#     style_normal = styles['Normal']
    
#     # Titre
#     title = Paragraph("Emploi du temps", style_title)
#     elements.append(title)
#     elements.append(Paragraph("<br/><br/>", style_normal))
    
#     # Récupération des données
#     seances = Seance.objects.all().select_related('module', 'groupe__filiere', 'salle', 'enseignant')
#     filieres = list(set([s.groupe.filiere for s in seances if s.groupe.filiere]))
    
#     # Créneaux horaires et jours
#     creneaux = [
#         ('08:30', '10:30'),
#         ('10:45', '12:45'),
#         ('14:00', '16:00'),
#         ('16:15', '18:15')
#     ]
#     jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
    
#     for filiere in filieres:
#         # Titre de la filière
#         elements.append(Paragraph(f"<b>Filière: {filiere.nom} - Semestre: {filiere.semestre}</b>", style_normal))
#         elements.append(Paragraph("<br/>", style_normal))
        
#         # Préparation des données du tableau
#         data = []
        
#         # En-tête avec les créneaux horaires
#         header = ['Jour/Horaire'] + [f"{debut}\nà\n{fin}" for debut, fin in creneaux]
#         data.append(header)
        
#         # Remplissage des données par jour
#         for jour in jours:
#             row = [jour]
#             for debut, fin in creneaux:
#                 cell_content = []
#                 for seance in seances:
#                     if (seance.groupe.filiere == filiere and 
#                         seance.jour == jour and 
#                         seance.heure_debut.strftime('%H:%M') == debut):
#                         cell_content.append(f"{seance.module.nom} ({seance.type_seance})")
#                         cell_content.append(f"Groupe: {seance.groupe.nom}")
#                         cell_content.append(f"Salle: {seance.salle.nom}")
#                         cell_content.append(f"Prof: {seance.enseignant.nom}")
                
#                 row.append('\n'.join(cell_content) if cell_content else '-')
#             data.append(row)
        
#         # Création du tableau
#         table = Table(data, colWidths=[80] + [120]*len(creneaux), rowHeights=30)
        
#         # Style du tableau
#         style = TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('FONTSIZE', (0, 0), (-1, 0), 10),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#             ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#         ])
        
#         table.setStyle(style)
#         elements.append(table)
#         elements.append(Paragraph("<br/><br/>", style_normal))
    
#     # Génération du PDF
#     doc.build(elements)
#     return response
    
def generer_groupes_pour_toutes_filieres(taille_groupe=35):
    Groupe.objects.all().delete()  # Réinitialiser tous les groupes

    filieres = Filiere.objects.all()
    for filiere in filieres:
        nb_etudiants = filiere.nombre_etudiants
        nb_groupes = -(-nb_etudiants // taille_groupe)  # division plafond
        for type_groupe in ['CM']:
          Groupe.objects.create(
                    nom=filiere.nom,
                    filiere=filiere,
                    type_groupe=type_groupe)
        
        for i in range(1, nb_groupes + 1):
            for type_groupe in ['TD', 'TP']:
                Groupe.objects.create(
                    nom=f"A{i}",
                    filiere=filiere,
                    type_groupe=type_groupe
                )
def generer_groupes(request):
    generer_groupes_pour_toutes_filieres()
    return redirect('liste_groupes') 






jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
creneaux = [
    (time(8, 30), time(10, 30)),
    (time(10, 45), time(12, 45)),
    (time(14, 00), time(16, 00)),
    (time(16, 15), time(18, 15)),
]
def conflit_existe(jour, debut, fin, enseignant, groupe, salle, module):
    return Seance.objects.filter(jour=jour, heure_debut=debut, heure_fin=fin).filter(
        Q(enseignant=enseignant) |
        Q(groupe=groupe) |
        Q(salle=salle) |
        Q(module=module) |
        # Conflit : même salle prise par autre filière au même moment
        ~Q(module__filiere=groupe.filiere) & Q(salle=salle) |
        # Conflit : même filière, même semestre => pas de chevauchement
        Q(module__filiere=module.filiere, module__filiere__semestre=module.filiere.semestre)
    ).exists()

def est_disponible(jour, debut, fin, enseignant, groupe, salle, module):
    if conflit_existe(jour, debut, fin, enseignant, groupe, salle, module):
     return False
    # Vérifie si l'enseignant est déjà occupé
    if Seance.objects.filter(jour=jour, heure_debut=debut, heure_fin__gt=debut, enseignant=enseignant).exists():
        return False

    # Vérifie si le groupe est déjà occupé
    if Seance.objects.filter(jour=jour, heure_debut=debut, heure_fin__gt=debut, groupe=groupe).exists():
        return False

    # Vérifie si la salle est déjà occupée
    if Seance.objects.filter(jour=jour, heure_debut=debut, heure_fin__gt=debut, salle=salle).exists():
        return False

    # Si la séance est un CM : aucun autre groupe de la même filière ne doit avoir de séance à ce moment
    if groupe.type_groupe == 'CM':
        if Seance.objects.filter(jour=jour, heure_debut=debut, heure_fin__gt=debut, module__filiere=groupe.filiere).exclude(groupe=groupe).exists():
            return False

    # Si ce n'est pas un CM : vérifier qu'aucun CM de la filière n'est en cours à ce moment
    else:
        if Seance.objects.filter(jour=jour, heure_debut=debut, heure_fin__gt=debut, type_seance='CM', module__filiere=groupe.filiere).exists():
            return False
   
    if groupe.type_groupe != 'CM':  # Vérifie que le groupe n'est pas un CM
    # Recherche si une autre séance existe avec les mêmes critères de jour, heure et filière
     if Seance.objects.filter(
        jour=jour, 
        heure_debut=debut, 
        heure_fin=fin, 
        module__filiere=groupe.filiere  # La filière doit correspondre à celle du groupe
    ).exclude(salle=salle, groupe=groupe).exists():  # Exclut la salle et le groupe actuel pour éviter un conflit
        return False  # Si une séance existe, retourne False pour indiquer qu'il y a un conflit

    return True




def backtrack_affectation(index, seances_a_generer):
    if index >= len(seances_a_generer):
        return True  # Tout est placé

    module, groupe = seances_a_generer[index]
    enseignant = module.enseignant
    type_seance = groupe.type_groupe

    for jour in jours:
        for debut, fin in creneaux:
            for salle in Salle.objects.all():
                # CM uniquement dans les salles de type 'CM'
                if type_seance == 'CM' and salle.type_salle != 'CM':
                    continue
                # TD/TP dans les autres types de salles
                if type_seance != 'CM' and salle.type_salle == 'CM':
                    continue
                if est_disponible(jour, debut, fin, enseignant, groupe, salle, module):
                    # Placer temporairement
                    seance = Seance.objects.create(
                        module=module,
                        enseignant=enseignant,
                        groupe=groupe,
                        salle=salle,
                        jour=jour,
                        heure_debut=debut,
                        heure_fin=fin,
                        type_seance=type_seance
                    )
                    # Récurse vers la suite
                    if backtrack_affectation(index + 1, seances_a_generer):
                        return True
                    # Retour arrière : annuler la séance
                    seance.delete()
    return False

def generer_emploi(request):
    Seance.objects.all().delete()

    seances_a_generer = []

    for filiere in set(Groupe.objects.values_list('filiere', flat=True)):
        # Générer une fois la séance CM pour chaque module de la filière
        groupes_cm = Groupe.objects.filter(filiere_id=filiere, type_groupe='CM')
        if groupes_cm.exists():
            groupe_cm = groupes_cm.first()  # Un seul groupe CM commun
            modules = Module.objects.filter(filiere_id=filiere)
            for module in modules:
                seances_a_generer.append((module, groupe_cm))

    # TD et TP : un par groupe
    for groupe in Groupe.objects.exclude(type_groupe='CM'):
        modules = Module.objects.filter(filiere=groupe.filiere)
        for module in modules:
            seances_a_generer.append((module, groupe))

    # Générer l'emploi du temps
    success = backtrack_affectation(0, seances_a_generer)

    if not success:
        print("Impossible de générer un emploi du temps complet")

    return redirect('emploi')



def liste_filieres(request):
    filieres = filieres = Filiere.objects.all()
    return render(request, 'liste.html', {'entites': filieres, 'titre': 'filieres'})

def liste_enseignants(request):
    enseignants = Enseignant.objects.all()
    return render(request, 'liste.html', {'entites': enseignants, 'titre': 'enseignants'})

def liste_modules(request):
    modules = Module.objects.all()
    return render(request, 'liste.html', {'entites': modules, 'titre': 'modules'})

def liste_salles(request):
    salles = Salle.objects.all()
    return render(request, 'liste.html', {'entites': salles, 'titre': 'salles'})

def liste_groupes(request):
    groupes = Groupe.objects.all()
    return render(request, 'liste.html', {'entites': groupes, 'titre': 'groupes'})

def liste_seances(request):
    seances = Seance.objects.all()
    return render(request, 'liste.html', {'entites': seances, 'titre': 'seances'})


def modifier_entite(request, model, form_class, pk, redirect_url):
    instance = get_object_or_404(model, pk=pk)
    form = form_class(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(redirect_url)
    return render(request, 'form.html', {'form': form})

def supprimer_entite(request, model, pk, redirect_url):
    instance = get_object_or_404(model, pk=pk)
    instance.delete()
    return redirect(redirect_url)

from .models import DisponibiliteEnseignant, DisponibiliteSalle

def afficher_contraintes(request):
    contraintes_ens = DisponibiliteEnseignant.objects.all()
    contraintes_salles = DisponibiliteSalle.objects.all()
    return render(request, 'contraintes.html', {
        'contraintes_ens': contraintes_ens,
        'contraintes_salles': contraintes_salles,
    })




# ENSEIGNANT
def liste_disponibilites_enseignants(request):
    disponibilites = DisponibiliteEnseignant.objects.all()
    return render(request, 'disponibilites/liste_enseignants.html', {'disponibilites': disponibilites})

def ajouter_disponibilite_enseignant(request):
    form = DisponibiliteEnseignantForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liste_disponibilites_enseignants')
    return render(request, 'form.html', {'form': form})

def modifier_disponibilite_enseignant(request, pk):
    dispo = get_object_or_404(DisponibiliteEnseignant, pk=pk)
    form = DisponibiliteEnseignantForm(request.POST or None, instance=dispo)
    if form.is_valid():
        form.save()
        return redirect('liste_disponibilites_enseignants')
    return render(request, 'form.html', {'form': form})

def supprimer_disponibilite_enseignant(request, pk):
    dispo = get_object_or_404(DisponibiliteEnseignant, pk=pk)
    dispo.delete()
    return redirect('liste_disponibilites_enseignants')

# SALLE
def liste_disponibilites_salles(request):
    disponibilites = DisponibiliteSalle.objects.all()
    return render(request, 'disponibilites/liste_salles.html', {'disponibilites': disponibilites})

def ajouter_disponibilite_salle(request):
    form = DisponibiliteSalleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liste_disponibilites_salles')
    return render(request, 'form.html', {'form': form})

def modifier_disponibilite_salle(request, pk):
    dispo = get_object_or_404(DisponibiliteSalle, pk=pk)
    form = DisponibiliteSalleForm(request.POST or None, instance=dispo)
    if form.is_valid():
        form.save()
        return redirect('liste_disponibilites_salles')
    return render(request, 'form.html', {'form': form})

def supprimer_disponibilite_salle(request, pk):
    dispo = get_object_or_404(DisponibiliteSalle, pk=pk)
    dispo.delete()
    return redirect('liste_disponibilites_salles')
    
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from .models import Seance, Filiere

# def exporter_pdf(request, filiere_id):
#     filiere = Filiere.objects.get(id=filiere_id)
#     seances = Seance.objects.filter(groupe__filiere=filiere).select_related('module', 'groupe', 'salle', 'enseignant')

#     creneaux = [
#         ('08:30', '10:30'),
#         ('10:45', '12:45'),
#         ('14:00', '16:00'),
#         ('16:15', '18:15')
#     ]
#     jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="Emploi_{filiere.nom}.pdf"'

#     doc = SimpleDocTemplate(response, pagesize=landscape(A4))
#     elements = []
#     styles = getSampleStyleSheet()

#     # Titre
#     titre = Paragraph(f"<strong>Emploi du temps — {filiere.nom} (Semestre {filiere.semestre})</strong>", styles['Title'])
#     elements.append(titre)
#     elements.append(Spacer(1, 12))

#     # Entête du tableau
#     data = [['Jour/Horaire'] + [f"{debut}\n{fin}" for debut, fin in creneaux]]

#     # Contenu du tableau
#     for jour in jours:
#         row = [jour]
#         for debut, fin in creneaux:
#             contenu = ""
#             for seance in seances:
#                 if seance.jour == jour and seance.heure_debut.strftime("%H:%M") == debut:
#                     contenu += f"{seance.module.nom}\n{seance.groupe.nom}\n{seance.salle.nom}\n{seance.enseignant.nom}\n({seance.type_seance})\n\n"
#             row.append(contenu.strip())
#         data.append(row)

#     # Création du tableau
#     table = Table(data, repeatRows=1)

#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f2f2f2")),
#         ('TEXTCOLOR',(0,0),(-1,0),colors.black),
#         ('ALIGN',(0,0),(-1,-1),'CENTER'),
#         ('FONTNAME', (0,0),(-1,0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0,0), (-1,-1), 10),  # Changer 8 à la taille désirée
#         ('BOX', (0,0), (-1,-1), 1, colors.black),
#         ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
#         ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
#         ('LEFTPADDING',(0,0),(-1,-1),4),
#         ('RIGHTPADDING',(0,0),(-1,-1),4),
#         ('TOPPADDING',(0,0),(-1,-1),4),
#         ('BOTTOMPADDING',(0,0),(-1,-1),4),
#     ]))

#     elements.append(table)
#     doc.build(elements)

#     return response
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from .models import Seance, Filiere

def exporter_pdf(request, filiere_id):
    filiere = Filiere.objects.get(id=filiere_id)
    seances = Seance.objects.filter(groupe__filiere=filiere).select_related('module', 'groupe', 'salle', 'enseignant')

    creneaux = [
        ('08:30', '10:30'),
        ('10:45', '12:45'),
        ('14:00', '16:00'),
        ('16:15', '18:15')
    ]
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Emploi_{filiere.nom}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(A4))
    elements = []
    styles = getSampleStyleSheet()

    # Titre avec style modifié
    titre_style = styles['Title']
    titre_style.fontSize = 14  # Réduit la taille de la police
    titre_style.leading = 16
    titre = Paragraph(f"<strong>Emploi du temps — {filiere.nom} (Semestre {filiere.semestre})</strong>", titre_style)
    elements.append(titre)
    elements.append(Spacer(1, 12))

    # Entête du tableau
    data = [['Jour/Horaire'] + [f"{debut}\n{fin}" for debut, fin in creneaux]]

    # Contenu du tableau
    for jour in jours:
        row = [jour]
        for debut, fin in creneaux:
            contenu = ""
            for seance in seances:
                if seance.jour == jour and seance.heure_debut.strftime("%H:%M") == debut:
                    contenu += f"{seance.module.nom}\n{seance.groupe.nom}\n{seance.salle.nom}\n{seance.enseignant.nom}\n({seance.type_seance})\n\n"
            row.append(contenu.strip())
        data.append(row)

    # Largeurs de colonnes personnalisées
    col_widths = [80] + [110] * len(creneaux)  # Réduit la largeur des colonnes

    # Hauteurs de lignes personnalisées
    row_heights = [30] + [60] * len(jours)  # Réduit la hauteur des lignes

    # Création du tableau avec dimensions personnalisées
    table = Table(data, colWidths=col_widths, rowHeights=row_heights, repeatRows=1)

    # Style amélioré pour économiser de l'espace
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f2f2f2")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        
        # Style en-tête
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
        
        # Style contenu
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 7),
        
        # Bordures
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        
        # Padding
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))

    elements.append(table)
    doc.build(elements)

    return response
