from django.db import models

JOUR_CHOICES = [
    ('Lundi', 'Lundi'),
    ('Mardi', 'Mardi'),
    ('Mercredi', 'Mercredi'),
    ('Jeudi', 'Jeudi'),
    ('Vendredi', 'Vendredi'),
    ('Samedi', 'Samedi'),
]

class Filiere(models.Model):
    nom = models.CharField(max_length=100)
    semestre = models.CharField(max_length=10, choices=[('S1', 'S1'), ('S2', 'S2'), ('S3', 'S3'), ('S4', 'S4'), ('S5', 'S5'), ('S6', 'S6')])
    nombre_etudiants = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nom} ({self.semestre})"

class Enseignant(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.nom

class Module(models.Model):
    nom = models.CharField(max_length=100)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True)
   
    def __str__(self):
        return self.nom

class Salle(models.Model):
    nom = models.CharField(max_length=50)
    capacite = models.IntegerField()
    type_salle = models.CharField(max_length=10, choices=[('CM', 'CM'), ('TD', 'TD'), ('TP', 'TP')])

    def __str__(self):
        return self.nom

class DisponibiliteEnseignant(models.Model):
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    jour = models.CharField(max_length=10)  
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

class DisponibiliteSalle(models.Model):
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    jour = models.CharField(max_length=10)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

class Groupe(models.Model):
    nom = models.CharField(max_length=100)
    type_groupe = models.CharField(max_length=2, choices=[('CM', 'CM'), ('TD', 'TD'), ('TP', 'TP')])
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.filiere.nom} ({self.filiere.semestre}) ({self.nom})({self.type_groupe})"

class Seance(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    jour = models.CharField(max_length=20)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    type_seance = models.CharField(max_length=2, choices=[('CM', 'CM'), ('TD', 'TD'), ('TP', 'TP')])

    def __str__(self):
        return f"{self.module.nom} - {self.jour} - {self.heure_debut}-{self.heure_fin} - {self.type_seance} - {self.groupe.nom}"

class EmploiDuTemps(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    date_heure = models.DateTimeField()
    type_seance = models.CharField(max_length=2, choices=[("CM", "CM"), ("TD", "TD"), ("TP", "TP")])  

