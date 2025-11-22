from django.urls import path

from .views import CategoriaPerguntaListView, CategoriaPerguntaCreateView, CategoriaPerguntaUpdateView, CategoriaPerguntaDeleteView
from .views import PerguntaListView, PerguntaCreateView, PerguntaUpdateView, PerguntaDeleteView
from .views import AlternativaListView, AlternativaCreateView, AlternativaUpdateView, AlternativaDeleteView
from .views import QuestionarioListView, QuestionarioCreateView, QuestionarioUpdateView, QuestionarioDeleteView #QuestionarioDetailView
from .views import ResponderQuestionarioView

urlpatterns = [
	path('categoria/list/', CategoriaPerguntaListView.as_view(), name='categoriapergunta_list'),
	path('categoria/cad/', CategoriaPerguntaCreateView.as_view(), name='categoriapergunta_create'),
	path('categoria/<slug:slug>/', CategoriaPerguntaUpdateView.as_view(), name='categoriapergunta_update'),
	path('categoria/<slug:slug>/delete/', CategoriaPerguntaDeleteView.as_view(), name='categoriapergunta_delete'), 
 
	path('pergunta/list/', PerguntaListView.as_view(), name='pergunta_list'),
	path('pergunta/cad/', PerguntaCreateView.as_view(), name='pergunta_create'),
	path('pergunta/<slug:slug>/', PerguntaUpdateView.as_view(), name='pergunta_update'),
	path('pergunta/<slug:slug>/delete/', PerguntaDeleteView.as_view(), name='pergunta_delete'),

	path('pergunta/<slug:pergunta_slug>/alternativa/', AlternativaListView.as_view(), name='alternativa_pergunta_list'),
	path('pergunta/<slug:pergunta_slug>/alternativa/cad', AlternativaCreateView.as_view(), name='alternativa_pergunta_create'),
	path('pergunta/alternativa/<slug:slug>/', AlternativaUpdateView.as_view(), name='alternativa_pergunta_update'),
	path('pergunta/alternativa/<slug:slug>/delete/', AlternativaDeleteView.as_view(), name='alternativa_pergunta_delete'),
 
 	path('questionario/list/', QuestionarioListView.as_view(), name='questionario_list'),
	path('questionario/cad/', QuestionarioCreateView.as_view(), name='questionario_create'),
	path('questionario/<slug:slug>/', QuestionarioUpdateView.as_view(), name='questionario_update'),
	path('questionario/<slug:slug>/delete/', QuestionarioDeleteView.as_view(), name='questionario_delete'),
 	path('questionario/responder/<slug:slug>/', ResponderQuestionarioView.as_view(), name='responder_questionario'),
]
