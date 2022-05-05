from django.template.defaultfilters import slugify
from gtts import gTTS
import os
from django.http import FileResponse, HttpResponse
from pathlib import Path
import datetime
from supermemo2 import SMTwo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializers import UserBookSerializer, WordTermSerializer
from .models import UserBook, WordTerm

# Create your views here.


class UserBookView(APIView):  # http://127.0.0.1:8000/api/words/
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        # user book de current user
        queryset = UserBook.objects.filter(user=request.user.id)
        # Envia el json correspondiente al queriset ed userbook actual
        serializer = UserBookSerializer(queryset, many=True)

        if(request.method == 'GET'):
            try:
                return Response(
                    {'success': serializer.data},
                    status=status.HTTP_200_OK
                )
            except:
                return Response(
                    {'error': 'error 505 algo no funciona correctamente', },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:

            return Response(
                {'error': 'No allow POST method ', },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# get translate, audio, and
# GET TRANSLATE
# 1.- pasar una palabra como argumento
#
# - [ ] traducciónes
# - [ ] scraping de google translate
# - [ ] get word
# - [ ] tranlate word
# - [ ] sinonyms > trans to trans
# - [ ] phrases


class SetWord(APIView):  # add Term http://127.0.0.1:8000/api/words/setword/
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        """POST, crea un nuevo objeto WordTerm y lo agrega al userbook del current user
        si este ya existe entonces lo encontramos y lo agregamos al current user book"""
        # queryset = Dictionary.objects.filter(user=request.user.id)
        try:
            data = request.data
            is_phrase = False
            if len(data.split()) > 1:
                is_phrase = True
            
            try:
                word = WordTerm.objects.get_or_create(word=data, phrase=is_phrase)

                try:
                    user_book = UserBook.objects.create(user=request.user, terms=word[0])
                    user_book.save()
                    return Response(
                        {'success': 'word add to dictionary and add to user book'},
                        status=status.HTTP_201_CREATED
                    )
                except:
                    return Response(
                        {'error': f'error 402 no puede crear un userbook con estos datos= user:{request.user} terms: {word[0]}'},
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
            except:
                return Response(
                    {'error': f'error 401 no puede crear o encontrar termino con estos datos= data:{data} phrase:{is_phrase}'},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
        except:
            return Response(
                {'error': f'error 400 neither added or created data:{request.data}'},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

# https://github.com/alankan886/SuperMemo2


class StudySession(APIView):  # http://127.0.0.1:8000/api/words/study_session/
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        data = request.data
        queryset = UserBook.objects.get(id=data['id'])
        # user = request.user
        # serializer = UserBookSerializer(queryset, many=True)
        today = datetime.date.today()  # only day

        # PRIMERA VES QUE SE ESTUDIA LA PALABRA
        if queryset.last_review == None:
            # review date would default to date.today() if not provided
            review = SMTwo.first_review(data['easiness'])
            # review prints SMTwo(easiness=2.36, interval=1, repetitions=1, review_date=datetime.date(2021, 3, 15))
            queryset.easiness = review.easiness
            queryset.interval = review.interval
            queryset.repetitions = review.repetitions
            queryset.next_review_date = review.review_date

        else:
            # ESTUDIAS LA PALABRA VARIAS VECES UN MISMO DIA
            if(queryset.last_review == today):
                queryset.repetitions = queryset.repetitions + 1
            # ESTUDIO FRECUENCIA NORMAL
            else:
                # other review
                review = SMTwo(queryset.easiness, queryset.interval,
                               queryset.repetitions).review(data['easiness'])
                queryset.easiness = review.easiness
                queryset.interval = review.interval
                queryset.repetitions = review.repetitions
                queryset.next_review_date = review.review_date

        queryset.last_review = today
        queryset.save()

        try:
            return Response(
                {'success': 'study session update'},
                status=status.HTTP_202_ACCEPTED
            )
        except:
            print('error 401 error de peticion try')
            return Response(
                {'error': 'error 505 neither added or created'},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )


class TextToSpeeshApi(APIView):  # http://127.0.0.1:8000/api/words/gttsApi/<arg>/
    permission_classes = [permissions.AllowAny]
    queryset = WordTerm.objects.all()
    serializer = WordTermSerializer(queryset, many=True)

    def get(self, request, word=None): # get word by url
        # mytext = request.data
        queryset = WordTerm.objects.filter(word=word)
        name = slugify(queryset[0])

        language = 'en'

        path = os.path.join((Path(__file__).resolve().parent.parent.parent), f'tem/{word}.ogg')
        path_exist = os.path.exists(path)

        if not path_exist: # create new audio
            audio = gTTS(text=name, lang=language)
            audio.save(path) 

        respose_audio = open(path, 'rb') # open
        response = FileResponse(respose_audio)
        # response['Content-Disposition'] = 'attachment; filename='somefilename.mp3'' # donwload

        return response


    # def post(self, request, word=None):
    #     mytext = request.data
    #     language = 'en'

    #     audio = gTTS(text=mytext, lang=language)
    #     audio.save(self.path)

    #     self.mytext = request.data

    #     return Response(
    #         {'success': 'text to speesh'},
    #         status=status.HTTP_202_ACCEPTED
    #     )

    # def get(self, request, format=None):
    #     respose_audio = open(self.path, 'rb')
    #     response = FileResponse(respose_audio)
    #     # response['Content-Disposition'] = 'attachment; filename='somefilename.mp3''

    #     return response
