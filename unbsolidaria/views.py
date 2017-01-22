from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DeleteView
from .models import Noticia, FAQ, Trabalho, User, Organizacao, Voluntario, Endereco
from django.core.mail import send_mail
from django.http import BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from .models import Noticia, FAQ,  UsuarioTrabalho
from django.template import RequestContext
from django.views import generic
from .forms import ContactForm, UserForm, OrganizacaoForm, VoluntarioForm, EnderecoForm, TrabalhoForm
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.urlresolvers import reverse_lazy
import django_filters

# Create your views here.

class IndexView(generic.ListView):
    template_name = '../templates/index.html'
    context_object_name = {}

    def get_queryset(self):
        return Noticia.objects.all()

class AboutView(generic.ListView):
    template_name = '../templates/about.html'
    context_object_name = {}

    def get_queryset(self):
        return Noticia.objects.all()


class OrganizacaoFormView(View):
    form_class = UserForm
    org_form_class = OrganizacaoForm
    endereco_class = EnderecoForm
    template_name = '../templates/cadastro/organizacao_form.html'    

    # mostrar um form em branco
    def get(self, request):
        form = self.form_class(None)
        org_form = self.org_form_class(None)
        endereco = self.endereco_class(None)

        return render(request, self.template_name, {'form': form, 'org_form': org_form, 'endereco': endereco})

    # processar informacoes
    def post(self, request):
        form = self.form_class(request.POST)
        org_form = self.org_form_class(request.POST)
        endereco = self.endereco_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)  # cria um objeto, porem n coloca no banco ainda

            # normaliza
            user.tipo = 1
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            if org_form.is_valid():
            	if endereco.is_valid():
          		user.save()
        		org_user = org_form.save(commit=False)  # cria um objeto, porem n coloca no banco ainda
                	end_user = endereco.save(commit=False)  # cria um objeto, porem n coloca no banco ainda
        	        org_user.organizacao_fk = user.id
               		end_user.usuario_fk = user.id
	                org_user.save()
	                end_user.save()

            # returna objeto se esta tudo certo com as credenciais
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:  # analisa se o usuario esta ativo, ou seja, n esta banido nem nada
                    login(request, user)
                    return redirect('../../')

        return render(request, self.template_name, {'form': form, 'org_form': org_form, 'endereco': endereco}) # se o usuario nao for valido, returna ele pro formulario de novo


class VoluntarioFormView(View):
    form_class = UserForm
    vol_form_class = VoluntarioForm
    endereco_class = EnderecoForm
    template_name = '../templates/cadastro/voluntario_form.html'

    # mostrar um form em branco
    def get(self, request):
        form = self.form_class(None)
        vol_form = self.vol_form_class(None)
        endereco = self.endereco_class(None)

        return render(request, self.template_name, {'form': form, 'vol_form': vol_form, 'endereco': endereco})

     # processar informacoes
    def post(self, request):
        form = self.form_class(request.POST)
        vol_form = self.vol_form_class(request.POST)
        endereco = self.endereco_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False )  # cria um objeto, porem n coloca no banco ainda
            # normaliza
            user.tipo = 0
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
	    
            user.set_password(password)
            if vol_form.is_valid():
		if endereco.is_valid():
			user.save()
             		vol_user = vol_form.save(commit=False)  # cria um objeto, porem n coloca no banco ainda
                	end_user = endereco.save(commit=False)  # cria um objeto, porem n coloca no banco ainda
             		vol_user.voluntario_fk = user.id
	                end_user.usuario_fk = user.id
	                end_user.save()
        	        vol_user.save()

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:  # analisa se o usuario esta ativo, ou seja, n esta banido nem nada
                    login(request, user)
                    return redirect('../../')

        return render(request, self.template_name, {'form': form, 'vol_form': vol_form, 'endereco': endereco})  # se o usuario nao for valido, returna ele pro formulario de novo


class UserUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = '../templates/cadastro/editUser.html'
    model = User
    fields = ['first_name', 'last_name', 'username', 'email', 'telefone', 
               'descricao']

    def get_object(self, queryset=None):
        return self.request.user


class UserDelete(LoginRequiredMixin, generic.DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = '../templates/trabalhos/deletarTrabalho.html'
    model = User
    success_url = reverse_lazy('../../')

    def get_object(self, queryset=None):
        return self.request.user


class PerfilUsuarioView(LoginRequiredMixin, generic.DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = '../templates/cadastro/perfil.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super(PerfilUsuarioView, self).get_context_data(**kwargs)
        return context

#######################################################################################
from django.core.mail import EmailMessage
from django.template.loader import get_template

def contato(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                template = get_template('contact_template.txt')
                content = template.render({
                    'subject': subject,
                    'from_email': from_email,
                    'message': message,
                })

                email = EmailMessage(
                    "Nova Mensagem Recebida",
                    content,
                    "UnBSolidaria" +'',
                    ['unbsolidariadesenv@gmail.com'],
                    headers = {'Reply-To': from_email }
                )
                email.send()
                form = ContactForm()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        return render_to_response("contato/contato.html", {'form': form,
                                                           'mensagem': 'Email enviado com sucesso!'},
                                  context_instance=RequestContext(request))
    return render(request, "contato/contato.html", {'form': form})


def faq(request):
    faq_list = FAQ.objects.all()
    paginator = Paginator(faq_list, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        perguntas = paginator.page(page)
    except (EmptyPage, InvalidPage):
        perguntas = paginator.page(paginator.num_pages)

    return render_to_response('faq/lista.html', {'perguntas': perguntas}, context_instance=RequestContext(request))


class DetailsNoticia(generic.DeleteView):
    model = Noticia
    template_name = 'noticia/noticia.html'


def noticias(request):
    noticias_list = Noticia.objects.all()
    paginator = Paginator(noticias_list, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        noticias = paginator.page(page)
    except (EmptyPage, InvalidPage):
        noticias = paginator.page(paginator.num_pages)

    return render_to_response('noticia/lista.html', {'noticias': noticias}, context_instance=RequestContext(request))


#######################################################################################
class TrabalhosView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = '../templates/trabalhos/listaTrabalhos.html'
    context_object_name = 'lista_trabalhos'
    paginate_by = 5	

    def get_queryset(self):
        user = self.request.user
        return Trabalho.objects.exclude(voluntarios=user)


class MeusTrabalhosView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = '../templates/trabalhos/meusTrabalhos.html'
    context_object_name = 'lista_trabalhos'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if self.request.user.tipo == 1:
            return super(MeusTrabalhosView, self).get(request, *args, **kwargs)
        else:
            return redirect('/listaTrabalhos')

    def get_queryset(self):
        return Trabalho.objects.all()



def ContribuicaoTrabalhosView(request):
        return render_to_response('trabalhos/contribuicaoTrabalhos.html', {'contribuicao_trabalhos': UsuarioTrabalho.objects.all(), 'lista_trabalhos': Trabalho.objects.all() }, context_instance=RequestContext(request))


class TrabalhoCreate(LoginRequiredMixin, generic.CreateView):
    trabalho_class = TrabalhoForm
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = '../templates/trabalhos/criarTrabalho.html'
    success_url = '/listaTrabalhos'

    def get(self, request):
        trabalho = self.trabalho_class(None)
        return render(request, self.template_name, {'trabalho': trabalho})

    def post(self, request):
        current_user = request.user
        trabalho = self.trabalho_class(request.POST)
        if trabalho.is_valid():
            trab = trabalho.save(commit=False )  # cria um objeto, porem n coloca no banco ainda
            trab.organizacao_id = current_user.id	
            trab.save()
	    return redirect('/meusTrabalhos/')	
	return render(request, self.template_name, {'trabalho': trabalho})


class TrabalhoUpdate(LoginRequiredMixin, generic.UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = '../templates/trabalhos/editarTrabalho.html'
    model = Trabalho
    fields = ['autor', 'email','titulo', 'descricao', 'vagas', 'data_inicio', 'data_fim']
    success_url = '/listaTrabalhos'

    def get(self, request, *args, **kwargs):
        if self.request.user.tipo == 1:
            return super(TrabalhoUpdate, self).get(request, *args, **kwargs)
        else:
            return redirect('/listaTrabalhos')


class TrabalhoDelete(LoginRequiredMixin, generic.DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = '../templates/trabalhos/deletarTrabalho.html'
    model = Trabalho
    success_url = reverse_lazy('lista-trabalhos')

    def get(self, request, *args, **kwargs):
        if self.request.user.tipo == 1:
            return super(TrabalhoDelete, self).get(request, *args, **kwargs)
        else:
            return redirect('/listaTrabalhos')


class TrabalhoDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = '../templates/trabalhos/visualizarTrabalho.html'
    model = Trabalho

    def get_context_data(self, **kwargs):
        context = super(TrabalhoDetailView, self).get_context_data(**kwargs)
        return context


#######################################################################################
class TrabalhoUsuarioCreate(generic.CreateView):
    template_name = '../templates/trabalhoUsuario/new.html'
    model = UsuarioTrabalho
    fields = ['organizacao', 'trabalho', 'voluntario']
    success_url = reverse_lazy('lista-trabalhos')

    def get_context_data(self, **kwargs):
        context = super(TrabalhoUsuarioCreate, self).get_context_data(**kwargs)
        teste = self.kwargs['pk']
        t = Trabalho.objects.get(pk=teste)
        t.decrement_vagas()
        context['trabalho'] = t
        return context


class TrabalhoUsuarioUpdate(LoginRequiredMixin, generic.UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = '../templates/trabalhoUsuario/update.html'
    model = UsuarioTrabalho
    fields = ['organizacao', 'trabalho', 'voluntario']
    success_url='/listaTrabalhos'


class TrabalhoUsuarioDelete(LoginRequiredMixin, generic.DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = '../templates/trabalhoUsuario/delete.html'
    model = UsuarioTrabalho
    success_url = reverse_lazy('lista-trabalhos')


class TrabalhoUsuarioView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = '../templates/trabalhoUsuario/list.html'
    context_object_name = 'lista_voluntarios'
    paginate_by = 5

    def get_queryset(self):
        teste = self.kwargs['pk']
        print teste
        return UsuarioTrabalho.objects.all().filter(trabalho_id=teste)

################################################################################

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            # 'sexo': ['exact'],
            'tipo': ['exact'],                     
        }

class TrabalhoFilter(django_filters.FilterSet):
    class Meta:
        model = Trabalho
        fields = {
            'vagas': ['exact'],
            'organizacao': ['exact'],
            'data_inicio': ['exact'],
            'data_fim': ['exact'],
        }

class UsuarioTrabalhoFilter(django_filters.FilterSet):
    class Meta:
        model = UsuarioTrabalho
        fields = {
            'organizacao': ['exact'],
            'trabalho': ['exact'],
            'voluntario': ['exact'],
        }

def filters(request):
    return render(request, 'filtros/filter.html')

def user_filters(request):
    f = UserFilter(request.GET, queryset=User.objects.all())
    return render(request, 'filtros/user.html', {'filter': f})

def trab_user_filters(request):
    f = UsuarioTrabalhoFilter(request.GET, queryset=UsuarioTrabalho.objects.all())
    # f = UserFilter(request.GET, queryset=User.objects.all())
    return render(request, 'filtros/trab_user.html', {'filter': f})

def trabalho_filters(request):
    g = TrabalhoFilter(request.GET, queryset=Trabalho.objects.all())
    return render(request, 'filtros/trab.html', {'filter': g})

from rest_framework import viewsets
from unbsolidaria.serializers import UserSerializer, TrabalhoSerializer, NoticiaSerializer, UsuarioTrabalhoSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class TrabalhoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Trabalho.objects.all()
    serializer_class = TrabalhoSerializer

class NoticiaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Noticia.objects.all()
    serializer_class = NoticiaSerializer

class UsuarioTrabalhoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UsuarioTrabalho.objects.all()
    serializer_class = UsuarioTrabalhoSerializer

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def get_user(request):
    if request.method == 'POST':
        request = request.body
        msg = json.loads(request)
        username = msg.get('username')
        user = User.objects.get(username = username)

        if user.tipo == 1:
            org = Organizacao.objects.get(organizacao_fk = user.id)
            postdata={'id':user.id, 'first_name':user.first_name, 'last_name':user.last_name, 'username':user.username,'tipo':user.tipo, 'descricao':user.descricao,'telefone':user.telefone,'cpf':'','cnpj':org.cnpj,'sexo':'','email':user.email}
        else:
            vol = Voluntario.objects.get(voluntario_fk = user.id)
            postdata={'id':user.id, 'first_name':user.first_name, 'last_name':user.last_name, 'username':user.username,'tipo':user.tipo, 'descricao':user.descricao,'telefone':user.telefone,'cpf':vol.cpf,'cnpj':'','sexo':vol.sexo,'email':user.email}

        return JsonResponse(postdata)

@csrf_exempt
def set_user(request):
    if request.method == 'PUT':
        request = request.body
        msg = json.loads(request)
        username = msg.get('username')
        user = User.objects.get(username = username)

        user.first_name = msg.get('first_name')
        user.last_name = msg.get('last_name')
        user.tipo = msg.get('tipo')
        user.descricao = msg.get('descricao')
        user.telefone = msg.get('telefone')
        user.save()

        if msg.get('tipo') == 1:
            org_obj = Organizacao.objects.filter(organizacao_fk = user.id).first()
            if org_obj is None:
                org_form = OrganizacaoForm().save(commit=False)
                org_form.organizacao_fk = user.id
                org_form.cnpj = msg.get('cnpj')
                org_form.save()
                return JsonResponse({'response': 'ok'})
            else:
                org_obj.cnpj = msg.get('cnpj')
                return JsonResponse({'response': 'edited'})
        else:
            vol_obj = Voluntario.objects.filter(voluntario_fk = user.id).first()
            if vol_obj is None:
                vol_form = VoluntarioForm().save(commit=False)
                vol_form.voluntario_fk = user.id
                vol_form.cpf = msg.get('cpf')
                vol_form.sexo = msg.get('sexo')
                vol_form.save()
                return JsonResponse({'response':'ok'})
            else:
                vol_obj.cpf = msg.get('cpf')
                vol_onj.sexo = msg.get('sexo')
                return JsonResponse({'response':'edited'})

@csrf_exempt
def edit_trabalho(request):
    if request.method == 'PUT':
        request = request.body
        msg = json.loads(request)
        titulo = msg.get('titulo')
        trab = Trabalho.objects.get(titulo = titulo)

        trab.titulo = msg.get('titulo')
        trab.descricao = msg.get('descricao')
        trab.autor = msg.get('autor')
        trab.email = msg.get('email')
        trab.data_inicio = msg.get('data_inicio')
        trab.data_fim = msg.get('data_fim')
        trab.vagas = msg.get('vagas')

        return JsonResponse({'response':'edited'})

from django.test.client import RequestFactory
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def show_trabs(request):
    if request.method == 'POST':
        body = request.body
        msg = json.loads(body)
        org = msg.get('organizacao')
        trabs = Trabalho.objects.filter(organizacao = org)
        # context = dict(request = RequestFactory().get('/'))

        # serializer = TrabalhoSerializer(trabs, many=True, context=context)
        serializer = TrabalhoSerializer(trabs, many=True, context={'request': request})
        return JSONResponse(serializer.data)



from easy_pdf.views import PDFTemplateView

class Pdf_trab(PDFTemplateView):
    template_name = "filtros/pdf_trab.html"

    def get_context_data(self, **kwargs):
        kwargs = {'trabs': Trabalho.objects.all()}
        return super(Pdf_trab, self).get_context_data(
            pagesize="A4",
            title="Trabalhos",
            **kwargs
        )
    
class Pdf_user(PDFTemplateView):
    template_name = "filtros/pdf_user.html"

    def get_context_data(self, **kwargs):
        kwargs = {'users': User.objects.all()}
        return super(Pdf_user, self).get_context_data(
            pagesize="A4",
            title="Users",
            **kwargs
        )

    
class Pdf_trab_user(PDFTemplateView):
    template_name = "filtros/pdf_trab_user.html"

    def get_context_data(self, **kwargs):
        kwargs = {'trabs': Trabalho.objects.all(), 'users': User.objects.all(), 'trab_user': UsuarioTrabalho.objects.all()}
        return super(Pdf_trab_user, self).get_context_data(
            pagesize="A4",
            title="Rel Trab/User",
            **kwargs
        )
