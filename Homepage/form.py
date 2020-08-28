from django import forms 
from .models import CountryName

class EnterCountry(forms.ModelForm):
    country_name = forms.CharField(max_length=29, widget=forms.TextInput(attrs={"placeholder": "Search country"}))
    
    class Meta:
        model = CountryName
        fields = ["country_name"]