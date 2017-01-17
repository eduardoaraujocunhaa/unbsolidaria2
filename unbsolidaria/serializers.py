from .models import User, Trabalho, Noticia, UsuarioTrabalho
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email', 'telefone') # Precisa de 'tipo', 'descricao', 'password' ??

class TrabalhoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trabalho
        fields = ('id', 'titulo', 'descricao', 'autor', 'email', 'vagas', 'data_inicio', 'data_fim', 'organizacao', 'voluntarios')

class NoticiaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Noticia
        fields = ('id', 'titulo', 'subtitulo', 'texto', 'dataCadastro', 'dataNoticia')

class UsuarioTrabalhoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
	    model = UsuarioTrabalho
	    fields = ('organizacao', 'voluntario', 'trabalho')