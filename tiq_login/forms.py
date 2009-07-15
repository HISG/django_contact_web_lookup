from django import forms

class PasswordChangeForm(forms.Form):
   
   username = forms.CharField(max_length=16)
   old_password = forms.CharField(max_length=16, widget=forms.PasswordInput)
   new_password_1 = forms.CharField(max_length=16, widget=forms.PasswordInput)
   new_password_2 = forms.CharField(max_length=16, widget=forms.PasswordInput)
   
   def clean(self):
      
      if (self.cleaned_data['new_password_1'] != self.cleaned_data['new_password_2']):
         raise forms.ValidationError("New Passwords must Match")

      return self.cleaned_data
      