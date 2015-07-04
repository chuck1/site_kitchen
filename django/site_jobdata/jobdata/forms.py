
from django import forms

class signup(forms.Form):
	username = forms.CharField(label="username", max_length=64)
	email = forms.CharField(label="email", max_length=256)
	pw1 = forms.CharField(label="password", max_length=64)
	pw2 = forms.CharField(label="password", max_length=64)

	def clean(self):
		cleaned_data = super(forms.Form, self).clean()
		pw1 = cleaned_data.get('pw1')
		pw2 = cleaned_data.get('pw2')

		if pw1 != pw2:
			raise forms.ValidationError(
				"password mismatch")
class login(forms.Form):
	username = forms.CharField(label="username", max_length=64)
	password = forms.CharField(label="password", max_length=64)

class document_render(forms.Form):
	options = forms.CharField(label="options"  ,  max_length=64)

class json_render(forms.Form):
	version  = forms.CharField(label="version",  max_length=64)
	

