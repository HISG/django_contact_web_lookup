from django import forms

class ContactSearchForm(forms.Form):
   
   search_term = forms.CharField(max_length=16)
