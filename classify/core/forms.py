from django import forms 
from core.models import UserFile


class FileForm(forms.ModelForm):
    class Meta():
        model = UserFile
        fields = {'title', 'file'}

    def file_dir(self):
        return str(self.cleaned_data['file'])