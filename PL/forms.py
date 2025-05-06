from django import forms
from .models import Filiere, Enseignant, Module, Salle, Groupe, Seance
from .models import  EmploiDuTemps

class FiliereForm(forms.ModelForm):
    class Meta:
        model = Filiere
        fields = '__all__'

class EnseignantForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = '__all__'

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = '__all__'

class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = '__all__'

class GroupeForm(forms.ModelForm):
    class Meta:
        model = Groupe
        fields = '__all__'

class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = '__all__'


class EnseignantLoginForm(forms.Form):
    nom = forms.CharField(label="Nom")
    email = forms.EmailField(label="Email")


