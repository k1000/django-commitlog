from django import forms


class CommitMessageForm(forms.Form):
	"""docstring for FileEditForm"""
	message = forms.CharField( widget=forms.Textarea, label="Commit Message" )

class TextFileEditForm(CommitMessageForm):
	"""docstring for FileEditForm"""
	file_source = forms.CharField( widget=forms.Textarea(attrs={'size':'60'}) )

class FileEditForm(CommitMessageForm):
	"""docstring for FileEditForm"""
	file_source = forms.FileField()

class FileDeleteForm(forms.Form):
	"""docstring for FileEditForm"""
	message = forms.CharField( widget=forms.HiddenInput )
	path = forms.CharField( widget=forms.HiddenInput )

class FileUploadForm(forms.Form):
	"""docstring for FileEditForm"""
	dir_path = forms.CharField( widget=forms.HiddenInput )
	file_source = forms.FileField( )

class RenameForm(forms.Form):
	"""docstring for FileEditForm"""
	new_name = forms.CharField()

class SearchForm(forms.Form):
	"""docstring for FileEditForm"""
	query = forms.CharField()