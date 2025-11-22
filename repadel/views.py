from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from formtools.wizard.views import SessionWizardView

from repadel.models import CategoriaPergunta, Pergunta, Alternativa, Questionario, Resposta

from utils.decorators import LoginRequiredMixin, TreinadorRequiredMixin

from .utils.prediction_engine import PredictionEngine

#Categoria
class CategoriaPerguntaListView(LoginRequiredMixin, TreinadorRequiredMixin, ListView):
    model = CategoriaPergunta
    template_name = 'repadel/categoriapergunta_list.html'

    
class CategoriaPerguntaCreateView(LoginRequiredMixin, TreinadorRequiredMixin, CreateView):
    model = CategoriaPergunta
    # form_class = CategoriaPerguntaForm
    fields = ['ordem', 'nome', 'descricao', 'is_active']
    
    success_url = 'categoriapergunta_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Categoria de pergunta cadastrada com sucesso na plataforma!')
        return reverse(self.success_url)
    
    
class CategoriaPerguntaUpdateView(LoginRequiredMixin, TreinadorRequiredMixin, UpdateView):
    model = CategoriaPergunta
    # form_class = CategoriaPerguntaForm
    fields = ['ordem', 'nome', 'descricao', 'is_active']
    success_url = 'categoriapergunta_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Categoria de pergunta atualizada com sucesso na plataforma!')
        return reverse(self.success_url)
    
   
class CategoriaPerguntaDeleteView(LoginRequiredMixin, TreinadorRequiredMixin, DeleteView):
    model = CategoriaPergunta
    
    success_url = 'categoriapergunta_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Categoria de pergunta removida com sucesso na plataforma!')
        return reverse(self.success_url)


    def post(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        
        try:
            self.object.delete()
            success_url = self.get_success_url()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à essa categoria, permissão negada!')
        return redirect(self.success_url)
    
    
#Pergunta
class PerguntaListView(LoginRequiredMixin, TreinadorRequiredMixin, ListView):
    model = Pergunta
    template_name = 'repadel/pergunta_list.html'

    
class PerguntaCreateView(LoginRequiredMixin, TreinadorRequiredMixin, CreateView):
    model = Pergunta    
    fields = ['ordem', 'texto', 'texto_exibido', 'tipo', 'categoria', 'obrigatoria', 'is_active']
    
    def get_success_url(self):
        messages.success(self.request, 'Pergunta cadastrada com sucesso na plataforma!')
        return self.object.get_alternativas_list_url
    
    
class PerguntaUpdateView(LoginRequiredMixin, TreinadorRequiredMixin, UpdateView):
    model = Pergunta
    fields = ['ordem', 'texto', 'texto_exibido', 'tipo', 'categoria', 'obrigatoria', 'is_active']
    template_name = 'repadel/pergunta_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Pergunta atualizada com sucesso na plataforma!')
        return self.object.get_alternativas_list_url
    
   
class PerguntaDeleteView(LoginRequiredMixin, TreinadorRequiredMixin, DeleteView):
    model = Pergunta
    success_url = 'pergunta_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Pergunta removida com sucesso na plataforma!')
        return reverse(self.success_url)


    def post(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        
        try:
            self.object.delete()
            success_url = self.get_success_url()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à essa pergunta, permissão negada!')
        return redirect(self.get_success_url())
    
#Alternativa à pergunta    
class AlternativaListView(LoginRequiredMixin, TreinadorRequiredMixin, ListView):
    model = Alternativa
    template_name = 'repadel/alternativa_list.html'

    def get_object(self):
        slug = self.kwargs.get('pergunta_slug')
        return Pergunta.objects.get(slug=slug)

    def get_context_data(self, *, object_list = ..., **kwargs):
        context = super().get_context_data(**kwargs)
        context['pergunta'] = self.get_object()
        return context

    def get_queryset(self):
        pergunta = self.get_object()
        return Alternativa.objects.filter(pergunta=pergunta).order_by('codigo')


class AlternativaCreateView(LoginRequiredMixin, TreinadorRequiredMixin, CreateView):
    model = Alternativa
    fields = ['codigo', 'texto']
    template_name = 'repadel/alternativa_form.html'

    def get_pergunta_object(self):
        slug = self.kwargs.get('pergunta_slug')
        return Pergunta.objects.get(slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pergunta'] = self.get_pergunta_object()
        return context

    def form_valid(self, form):
        formulario = form.save(commit=False)
        formulario.pergunta = self.get_pergunta_object()
        formulario.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Alternativa cadastrada com sucesso na plataforma!')
        return self.object.pergunta.get_alternativas_list_url


class AlternativaUpdateView(LoginRequiredMixin, TreinadorRequiredMixin, UpdateView):
    model = Alternativa
    fields = ['codigo', 'texto']
    template_name = 'repadel/alternativa_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Alternativa atualizada com sucesso na plataforma!')
        return self.object.pergunta.get_alternativas_list_url


class AlternativaDeleteView(LoginRequiredMixin, TreinadorRequiredMixin, DeleteView):
    model = Alternativa

    def get_success_url(self):
        messages.success(self.request, 'Alternativa removida com sucesso na plataforma!')
        return self.object.pergunta.get_alternativas_list_url

    def post(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()

        try:
            self.object.delete()
            success_url = self.get_success_url()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à essa alternativa, permissão negada!')
        return redirect(self.get_success_url())
    
    
#Questionario
class QuestionarioListView(LoginRequiredMixin, TreinadorRequiredMixin, ListView):
    model = Questionario
    template_name = 'repadel/questionario_list.html'

    
class QuestionarioCreateView(LoginRequiredMixin, TreinadorRequiredMixin, CreateView):
    model = Questionario    
    fields = ['titulo', 'descricao', 'perguntas', 'is_active']
    success_url = 'questionario_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Questionário cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)
    
    
class QuestionarioUpdateView(LoginRequiredMixin, TreinadorRequiredMixin, UpdateView):
    model = Questionario
    fields = ['titulo', 'descricao', 'perguntas', 'is_active']
    template_name = 'repadel/questionario_form.html'
    success_url = 'questionario_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Questionário atualizado com sucesso na plataforma!')
        return reverse(self.success_url)
    
   
class QuestionarioDeleteView(LoginRequiredMixin, TreinadorRequiredMixin, DeleteView):
    model = Questionario
    success_url = 'questionario_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Questionario removido com sucesso na plataforma!')
        return reverse(self.success_url)

    def post(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        
        try:
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à esse pergunto, permissão negada!')
        return redirect(self.get_success_url())


# Resultado
class RespostaCreateView(CreateView):
    model = Resposta
    fields = ['questionario', 'pergunta', 'alternativa', 'resposta_texto', 'respondente']  # o formulário será montado manualmente no template
    template_name = 'repadel/resposta_form.html'
    # success_url = reverse_lazy('resultado_recomendacao')
    success_url = reverse_lazy('repadel:resultado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perguntas'] = Pergunta.objects.select_related('categoria').prefetch_related('alternativas').order_by('categoria__nome', 'id')
        return context

    def post(self, request, *args, **kwargs):
        perguntas = Pergunta.objects.all().prefetch_related('alternativas')
        # atleta logado (ver caso 1 ou 2 acima)
        atleta = request.user
        respostas_dict = {}
        for pergunta in perguntas:
            chave = f"pergunta_{pergunta.id}"
            alternativa_id = request.POST.get(chave)
            if alternativa_id:
                alternativa = Alternativa.objects.get(pk=alternativa_id)
                Resposta.objects.create(atleta=atleta, pergunta=pergunta, alternativa=alternativa)
                respostas_dict[pergunta.texto] = alternativa.valor

        # Executa predição
        resultado = PredictionEngine.prever_categoria(respostas_dict)

        # (opcional) salvar categoria prevista no perfil do atleta
        if hasattr(atleta, 'categoria_prevista'):
            atleta.categoria_prevista = resultado['categoria_prevista']
            atleta.detalhes = resultado['detalhes']
            atleta.save()

        return render(request, 'repadel/resultado.html', {
            'atleta': atleta,
            'categoria_prevista': resultado['categoria_prevista'],
            'detalhes': resultado['detalhes'],
        })
    
#Responder Questionario
class ResponderQuestionarioView(View):
    template_name = "repadel/responder_questionario_form.html"

    def get_current_page(self, request):
        if request.method == "POST":
            return int(request.POST.get("page", 1))
        return int(request.GET.get("page", 1))

    def get_categorias(self, questionario):
        return list(
            questionario.perguntas
            .order_by("categoria__ordem")
            .values_list("categoria__nome", flat=True)
            .distinct()
        )

    def get(self, request, slug):
        questionario = get_object_or_404(Questionario, slug=slug)

        categorias = self.get_categorias(questionario)

        page = self.get_current_page(request)

        # Evitar acessar páginas inexistentes
        if page < 1:
            page = 1
        if page > len(categorias):
            return redirect(f"{request.path}?page=1")

        categoria_atual = categorias[page - 1]

        perguntas = questionario.perguntas.filter(categoria__nome=categoria_atual)

        return render(request, self.template_name, {
            "questionario": questionario,
            "perguntas": perguntas,
            "page": page,
            "total_pages": len(categorias),
            "categoria_atual": categoria_atual
        })


    def post(self, request, slug):
        questionario = get_object_or_404(Questionario, slug=slug)
        page = self.get_current_page(request)

        categorias = self.get_categorias(questionario)
        categorias = list(categorias)

        categoria_atual = categorias[page - 1]
        perguntas = questionario.perguntas.filter(categoria__nome=categoria_atual)

        # Recuperar dicionário acumulado da sessão
        respostas_acumuladas = request.session.get("respostas_temp", {})

        autoavaliacao = request.session.get("autoavaliacao")

        # Ler respostas desta página
        for pergunta in perguntas:
            key = f"pergunta_{pergunta.id}"
            valor = request.POST.get(key)

            if not valor:
                continue

            if pergunta.tipo == "MULTIPLA_ESCOLHA":
                alt = Alternativa.objects.get(pk=valor)
                texto_resposta = alt.texto
            else:
                texto_resposta = valor

            respostas_acumuladas[f"{pergunta.categoria.nome} : {pergunta.texto}"] = texto_resposta

            # SE FOR AUTOAVALIAÇÃO, SALVAR SEPARADO
            if pergunta.categoria.nome.upper() == "AUTOAVALIACAO":
                autoavaliacao = texto_resposta
                request.session["autoavaliacao"] = autoavaliacao

        # Salvar respostas acumuladas
        request.session["respostas_temp"] = respostas_acumuladas

        # Se houver próxima página → redirecionar
        if page < len(categorias):
            return redirect(f"{request.path}?page={page + 1}")

        # Última página → processar tudo
        respostas_final = respostas_acumuladas

        # Limpar
        request.session.pop("respostas_temp", None)
        autoavaliacao = request.session.pop("autoavaliacao", None)

        # Executar predição
        resultado = PredictionEngine.prever_categoria(respostas_final)

        atleta = request.user

        return render(request, "repadel/resultado.html", {
            "atleta": atleta,
            "categoria_prevista": resultado["categoria_prevista"],
            "detalhes": resultado["detalhes"],
            "autoavaliacao": autoavaliacao,   # <-- AGORA DISPONÍVEL NO HTML
        })
    

    