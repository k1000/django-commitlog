from django import forms

# place form definition here

class CommitMessageForm(forms.Form):
	"""docstring for FileEditForm"""
	message = forms.CharField( widget=forms.Textarea, label="Commit Message" )

class TextFileEditForm(CommitMessageForm):
	"""docstring for FileEditForm"""
	file_source = forms.CharField( widget=forms.Textarea(attrs={'size':'60'}) )
			

class FileEditForm(CommitMessageForm):
	"""docstring for FileEditForm"""
	file_source = forms.FileField()

class FileDeleteForm(CommitMessageForm):
	"""docstring for FileEditForm"""
	path = forms.CharField( widget=forms.HiddenInput )

class FileUploadForm(forms.Form):
	"""docstring for FileEditForm"""
	file_source = forms.FileField( )

class RenameForm(forms.Form):
	"""docstring for FileEditForm"""
	new_name = forms.CharField()
		