from django import forms
from adminCine.models import Sala

class FormularioSalas(forms.ModelForm):
    class Meta:
        model = Sala

        fields = [
        'id_sala',
        'nombre',
        'activo',
        'filas',
        'asientos',

        ]

        labels = { 'id_sala': 'ID',
        'nombre':'Nombre',
        'activo': 'Activo',
        'filas':'Filas',
        'asientos':'Asientos'}

    """     widgets = {
        'nombre': forms.TextInput(),
        'activo':forms.BooleanField(),
        'filas':forms.TextInput(),
        'asientos':forms.TextInput()
        }
     """

    id_sala = forms.IntegerField(required = False,widget=forms.TextInput(attrs={'readonly':'readonly','placeholder':'ID autogenerado'}))   
    nombre = forms.CharField()
    activo = forms.BooleanField(required=False)
    filas = forms.IntegerField()
    asientos = forms.IntegerField()
