from django.urls import path
from .views import (FlashCardView, SetFlashCard, UpdateDb,
                    TextToSpeeshApi, StudySession, GetTranslateApi,)

urlpatterns = [
    # http://127.0.0.1:8000/api/words/
    path("", FlashCardView.as_view()),

    # http://127.0.0.1:8000/api/words/1/
    path("id/<pk>/", SetFlashCard.as_view()),

    # http://127.0.0.1:8000/api/words/updatedb/
    # path('updatedb/', UpdateDb.as_view()),

    # http://127.0.0.1:8000/api/words/study_session/
    path("study_session/", StudySession.as_view()),

    # http://127.0.0.1:8000/api/words/gttsApi/test/
    path("gttsApi/<word>/", TextToSpeeshApi.as_view()),

    # http://127.0.0.1:8000/api/words/translate/test/
    path("translate/<word>/", GetTranslateApi.as_view()),
]
