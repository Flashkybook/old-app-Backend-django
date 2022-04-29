from django.urls import path
from .views import ViewUserBook, AddWordTerms, StudyWordSession, TextToSpeeshApi

urlpatterns = [
    path('', ViewUserBook.as_view()), # http://127.0.0.1:8000/api/words/
    path('add_to_dict/', AddWordTerms.as_view()), # http://127.0.0.1:8000/api/words/add_to_dict/  
    path('study_session/', StudyWordSession.as_view()), # http://127.0.0.1:8000/api/words/study_session/
    path('text_to_speesh/', TextToSpeeshApi.as_view()), # http://127.0.0.1:8000/api/words/text_to_speesh/
]
