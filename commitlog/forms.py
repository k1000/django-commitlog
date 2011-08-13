from django import forms

# place form definition here

class TextFileEditForm(forms.Form):
	"""docstring for FileEditForm"""
	
	file_source = forms.CharField( widget=forms.Textarea(attrs={'size':'60'}) )
	message = forms.CharField( widget=forms.Textarea )

class FileEditForm(forms.Form):
	"""docstring for FileEditForm"""
	
	file_source = forms.FileField()
	message = forms.CharField( widget=forms.Textarea )
		