from django import forms
from web.models import User


class ModelFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class PdfForm(forms.Form):
    url = forms.URLField(
        widget=forms.URLInput(
        attrs={
            'class': 'form-control'
            }
        )
    )


class UserRegistrationForm(ModelFormMixin, forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class AuthForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ))


class EditForm(forms.Form):
    new_email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control'
        }), required=False)
    new_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }), required=False)
    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }), required=False)
