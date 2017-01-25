# -*- coding: utf-8 -*-
from models import User, Organizacao, Voluntario, Trabalho, Endereco, Feedback
from django import forms
from localflavor.br.forms import BRCPFField, BRCNPJField, BRPhoneNumberField, BRZipCodeField

class ContactForm(forms.Form):
    INPUT_CLASS = 'form-control input-lg'

    from_email = forms.EmailField(required=True,
                                  widget=forms.EmailInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Email*'}))
    subject = forms.CharField(required=True,
                              widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Assunto*'}))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':INPUT_CLASS,'placeholder': 'Mensagem*'}))



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    telefone = BRPhoneNumberField(required=True, widget=forms.TextInput(attrs={'data-mask': '(00)00000-0000', 'class': '.phone', 'placeholder':'(__)_____-____'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'telefone', 'descricao']


class OrganizacaoForm(forms.ModelForm):
    cnpj = BRCNPJField(required=True, widget=forms.TextInput(attrs={'placeholder':'__.___.___/____-__'}))
    class Meta:
        model = Organizacao
        fields = ['cnpj']


class VoluntarioForm(forms.ModelForm):
    cpf = BRCPFField(required=True, widget=forms.TextInput(attrs={'placeholder':'___.___.___.___-__'}))

    class Meta:
        model = Voluntario
        fields = ['cpf', 'sexo']


class EnderecoForm(forms.ModelForm):
    cep = BRZipCodeField(required=True, widget=forms.TextInput(attrs={'placeholder':'______-___'}))
    class Meta:
        model = Endereco
        fields = ['endereco', 'cep']


class TrabalhoForm(forms.ModelForm):
    class Meta:
        model = Trabalho
 	fields = ['titulo', 'descricao', 'autor', 'email', 'vagas', 'data_inicio', 'data_fim']


class FeedBackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['titulo', 'descricao']