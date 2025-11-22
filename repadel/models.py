from django.apps import apps
from django.db import models
from django.urls import reverse

from usuario.models import Usuario

from utils.gerador_hash import gerar_hash


class CategoriaPerguntaAtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)  


class CategoriaPergunta(models.Model):
    ordem = models.PositiveIntegerField('Ordem', null=True, blank=False)
    nome = models.CharField('Título', max_length=100)
    descricao = models.CharField('Descrição ou uma explicação sobre a categoria', max_length=500)
    is_active = models.BooleanField('Ativo', default=True, help_text='Se ativa, pode ser utilizada.')
    slug = models.SlugField('Hash', max_length= 200,null=True,blank=True)
    
    objects = models.Manager()
    categorias_ativas = CategoriaPerguntaAtivoManager()
    

    class Meta:
        ordering = ['-is_active','ordem']
        unique_together = [['nome']]
    
    def __str__(self):
        return f"{self.nome}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        self.nome = self.nome.upper()
        super(CategoriaPergunta, self).save(*args, **kwargs)
    
    @property
    def get_absolute_url(self):
        return reverse('categoriapergunta_update', kwargs={'slug': self.slug})
    
    @property
    def get_delete_url(self):
        return reverse('categoriapergunta_delete', kwargs={'slug': self.slug})


class Pergunta(models.Model):
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    TIPOS = (
        ('TEXTO', 'Resposta Aberta (texto)'),
        ('NUMERICA', 'Resposta Numérica' ),
        ('MULTIPLA_ESCOLHA', 'Múltipla Escolha' ),        
    )
    ordem = models.PositiveIntegerField('Ordem', null=True, blank=False)
    texto = models.CharField('Texto', max_length=255)
    texto_exibido = models.CharField('Texto exibido', null=True, blank=True, max_length=255)
    tipo = models.CharField('Tipo', max_length=20, choices=TIPOS, default='MULTIPLA_ESCOLHA')
    categoria = models.ForeignKey(CategoriaPergunta, verbose_name='Categoria', on_delete=models.RESTRICT, related_name="categoria")
    obrigatoria = models.BooleanField('Obrigatória?', default=True)
    is_active = models.BooleanField('Ativo', default=True, help_text='Se ativa, pode ser utilizada.')
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    
    class Meta:
        ordering            = ['-is_active', 'categoria', 'ordem']
        unique_together     = [['categoria', 'texto']]
        verbose_name        = ('pergunta')
        verbose_name_plural = ('perguntas')

    def __str__(self):
        return f"{self.categoria} : {self.texto}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        super(Pergunta, self).save(*args, **kwargs)
    
    @property
    def get_absolute_url(self):
        return reverse('pergunta_update', kwargs={'slug': self.slug})
    
    @property
    def get_delete_url(self):
        return reverse('pergunta_delete', kwargs={'slug': self.slug})

    @property
    def get_alternativas_list_url(self):
        return reverse('alternativa_pergunta_list', kwargs={'pergunta_slug': self.slug})

    @property
    def get_alternativas_create_url(self):
        return reverse('alternativa_pergunta_create', kwargs={'pergunta_slug': self.slug})


class Alternativa(models.Model):
    pergunta = models.ForeignKey(Pergunta, verbose_name='Pergunta associada', on_delete=models.RESTRICT, related_name="pergunta")
    codigo = models.PositiveSmallIntegerField('Código')  # Ex.: 1, 2, 3...
    texto = models.CharField('Alternativa para a pergunta. Ex.: Feminino, Masculino', max_length=100)     # Ex.: "Feminino", "Masculino"
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)

    class Meta:
        unique_together     = [['pergunta', 'codigo']]
        ordering            = ['codigo']
        verbose_name        = ('alternativa')
        verbose_name_plural = ('alternativas')

    def __str__(self):
        return f"{self.codigo}) {self.pergunta} : {self.texto}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        super(Alternativa, self).save(*args, **kwargs)
    
    @property
    def get_absolute_url(self):
        return reverse('alternativa_pergunta_update', kwargs={'slug': self.slug})
    
    @property
    def get_delete_url(self):
        return reverse('alternativa_pergunta_delete', kwargs={'slug': self.slug})
    
    
class Questionario(models.Model):
    titulo = models.CharField('Título do questionário/enquete', max_length=200)
    descricao = models.TextField('Descrição', blank=True, null=True)
    perguntas = models.ManyToManyField(Pergunta, verbose_name='Selecione as perguntas para o questionário', related_name="perguntas")
    criado_em = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField('Ativo', default=True, help_text='Se ativo, pode ser utilizado.')
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)
    
    
    class Meta:
        unique_together     = [['titulo']]
        ordering            = ['titulo']
        verbose_name        = ('questionário')
        verbose_name_plural = ('questionários')

    def __str__(self):
        return f"{self.titulo}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        super(Questionario, self).save(*args, **kwargs)
    
    @property
    def get_absolute_url(self):
        return reverse('questionario_update', kwargs={'slug': self.slug})
    
    @property
    def get_delete_url(self):
        return reverse('questionario_delete', kwargs={'slug': self.slug})
    
    @property
    def get_visualiza_questionario_url(self):
        return reverse('questionario_detail', kwargs={'slug': self.slug})
    
    @property
    def total_perguntas(self):
        return self.perguntas.count()
    
    @property
    def get_responder_url(self):
        return reverse('responder_questionario', kwargs={'slug': self.slug})
    
    @property
    def get_responder_appatleta_url(self):
        return reverse('appatleta_responder_questionario', kwargs={'slug': self.slug})
    


class Resposta(models.Model):
    questionario = models.ForeignKey(Questionario, on_delete=models.RESTRICT, related_name="questionario")
    pergunta = models.ForeignKey(Pergunta, on_delete=models.RESTRICT, related_name="pergunta_resposta")
    alternativa = models.ForeignKey(Alternativa, on_delete=models.SET_NULL, blank=True, null=True, related_name='alternativa')
    resposta_texto = models.TextField('Texto da resposta', blank=True, null=True)  # Para perguntas abertas
    respondente = models.ForeignKey(Usuario, verbose_name='Atleta', on_delete=models.RESTRICT, related_name="respondente")
    respondido_em = models.DateTimeField(auto_now_add=True)

    class Meta:        
        unique_together     = [['questionario', 'pergunta']]
        ordering            = ['questionario', 'pergunta']
        verbose_name        = ('resposta')
        verbose_name_plural = ('respostas')

    def __str__(self):
        return f"Resposta {self.id}: {self.questionario}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        super(Resposta, self).save(*args, **kwargs)
    
    @property
    def get_absolute_url(self):
        return reverse('resposta_update', kwargs={'slug': self.slug})
    
    @property
    def get_delete_url(self):
        return reverse('resposta_delete', kwargs={'slug': self.slug})
    