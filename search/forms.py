from django import forms

# Source: https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/
class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

# Source: https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

# Source: https://stackoverflow.com/questions/5871730/how-to-upload-a-file-in-django
class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

# Source: https://django-elasticsearch-dsl.readthedocs.io/en/latest/quickstart.html