from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    tag = forms.CharField(label='Tag', max_length=100)

class UnknownSpecter(forms.Form):
	docfile = forms.ImageField(
		label='Select spectral image',
		help_text='max. 42 megabytes'
	)
	