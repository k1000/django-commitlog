from django import forms

# place form definition here

class FileEditForm(forms.Form):
	"""docstring for FileEditForm"""
	
	file_source = forms.CharField( widget=forms.Textarea )
	message = forms.CharField( widget=forms.Textarea )
		