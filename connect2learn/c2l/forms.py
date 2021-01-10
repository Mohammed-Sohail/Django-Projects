from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import c2lUser

class RegForm(UserCreationForm):
    email=forms.EmailField(label='Email')
    phone= forms.IntegerField(label='Phone Number')
    address=forms.CharField(label='Address',widget=forms.Textarea(attrs={"rows":1, "cols":30}),required=False)
    
    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1','password2']:
            self.fields[fieldname].help_text = None
        self.fields['first_name'].required= True

    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2','first_name','last_name','phone']
