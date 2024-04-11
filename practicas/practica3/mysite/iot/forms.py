from django import forms
from .models import *

class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ['description', 'condition', 'action', 'created_at']
