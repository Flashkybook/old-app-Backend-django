from django.urls import path
from .views import UserBookView, SetUserBook,  TextToSpeeshApi, StudySession

urlpatterns = [
    path('', UserBookView.as_view()), # http://127.0.0.1:8000/api/words/
    path('<pk>/', SetUserBook.as_view()), # http://127.0.0.1:8000/api/words/setword/  
    path('study_session/', StudySession.as_view()), # http://127.0.0.1:8000/api/words/study_session/
    path('gttsApi/<word>/', TextToSpeeshApi.as_view()), # http://127.0.0.1:8000/api/words/gttsApi/
]
