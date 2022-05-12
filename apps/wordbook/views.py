import os
import datetime
from pathlib import Path
from gtts import gTTS
from supermemo2 import SMTwo

from django.template.defaultfilters import slugify
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404

# Django Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

# models and serializer
from .serializers import UserBookSerializer, WordTermSerializer
from .models import UserBook, WordTerm


class UserBookView(APIView):  # http://127.0.0.1:8000/api/words/
    permission_classes = (permissions.AllowAny,)

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


    def post(self, request, format=None):
        """crea un nuevo objeto WordTerm y lo agrega al userbook del current user
        si este ya existe entonces lo encontramos y lo agregamos al current user book"""

        try:
            data = request.data
            data = data.strip()
            print(data)
            is_phrase = False
            if len(data.split()) > 1:
                is_phrase = True
            word_exist = WordTerm.objects.filter(word=data).exists()
            if not word_exist:  # si no existe crea el termino y lo agrega a userbook
                try:
                    word = WordTerm.objects.create(word=data, phrase=is_phrase)
                    word.save()
                    try:
                        # Lo agrega al user book
                        user_book = UserBook.objects.create(
                            user=request.user, terms=word)
                        user_book.save()
                        return Response(
                            {'success': "word created and add to user book"},
                            status=status.HTTP_202_ACCEPTED
                        )
                    except:
                        return Response(
                            {
                                'error': f'error 403 cannot create user_book with => user:{request.user} terms:{word}'
                            },
                            status=status.HTTP_406_NOT_ACCEPTABLE
                        )
                except:
                    return Response(
                        {
                            'error': f'error 404 cannot create word with => data:{data}, phrase:{is_phrase}'
                        },
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
            else:
                word = WordTerm.objects.get(word=data)
                try:
                    user_book_exist = UserBook.objects.filter(
                        user=request.user, terms=word)
                    if not user_book_exist:
                        # Lo agrega al user book
                        try:
                            user_book = UserBook.objects.create(
                                user=request.user, terms=word)
                            user_book.save()
                            return Response(
                                {'success': "word add to user book"},
                                status=status.HTTP_202_ACCEPTED
                            )

                        except:
                            return Response(
                                {
                                    'error': f'error 403 cannot create user_book with => user:{request.user}, word:{word}'
                                },
                                status=status.HTTP_406_NOT_ACCEPTABLE
                            )
                except:
                    return Response(
                        {
                            'error': f'error 403 cannot get word with => word:{data}'
                        },
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
                else:
                    return Response(
                        {'error': "402 already exist in your userbook"},
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
        except:
            return Response(
                {
                    'error': f'error 401 => {data}'
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )


class SetUserBook(APIView):  # add Term http://127.0.0.1:8000/api/words/setword/
    permission_classes = (permissions.AllowAny,)

    def delete(self, request, pk, format=None):
        
        user_book = get_object_or_404(UserBook, user=request.user, id=pk)
        # only can delete this word if this word is only used by this user
        if(user_book.terms.users.count() == 1):
            word = WordTerm.objects.get(word=user_book.terms.word)
            word.delete()
        else:
            user_book.delete()


        return Response(
            {'success': f'{user_book} delete success'},
            status=status.HTTP_202_ACCEPTED
        )


class StudySession(APIView):  # http://127.0.0.1:8000/api/words/study_session/
    # https://github.com/alankan886/SuperMemo2

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = request.data
        queryset = UserBook.objects.get(id=data['id'])

        today = datetime.date.today()  # only day

        # if data['fails'] > 5:
        #     data['fails'] = 5
        print(data)

        # PRIMERA VES QUE SE ESTUDIA LA PALABRA
        if queryset.last_review == None:
            # review date would default to date.today() if not provided
            review = SMTwo.first_review(5 - data['fails'])
            # review prints SMTwo(easiness=2.36, interval=1, repetitions=1, review_date=datetime.date(2021, 3, 15))

            # save data of SMTwo in queryset
            queryset.easiness = review.easiness
            queryset.interval = review.interval
            queryset.repetitions = review.repetitions
            queryset.next_review_date = review.review_date

        else:
            # WORD STUDY MANY TIMES AT SAME DAY
            if(queryset.last_review == today):
                print(queryset.repetitions + 1)
                queryset.repetitions = queryset.repetitions + 1

            # NORMAL STUDY FREQUENCY
            else:
                # other review
                review = SMTwo(float(queryset.easiness), queryset.interval,
                               queryset.repetitions).review(5 - data['fails'])
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
    permission_classes = (permissions.AllowAny,)
    queryset = WordTerm.objects.all()
    serializer = WordTermSerializer(queryset, many=True)

    if not os.path.exists('/tmp'):
        os.mkdir('/tmp')
        print('create /tmp', os.path.exists('/tmp'))

    def get(self, request, word):  # get word by url
        queryset = WordTerm.objects.filter(word=word)
        name = slugify(queryset[0])
        language = 'en'

        # local tmp root
        local = os.path.join(
            (Path(__file__).resolve().parent.parent.parent), f'tmp/')
        if os.path.exists(local):
            path = os.path.join(
                (Path(__file__).resolve().parent.parent.parent), f'tmp/{word}.ogg')

        # dev tmp root
        else:
            path = os.path.join(f'/tmp/{word}.ogg')

        # check file exist or file size is 0KB for create new audio
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            audio = gTTS(text=name, lang=language)
            audio.save(path)

        respose_audio = open(path, 'rb')  # open
        response = FileResponse(respose_audio)

        # response['Content-Disposition'] = 'attachment; filename='somefilename.mp3' # for donwload file
        return response


class GetTranslateApi(APIView):  # http://127.0.0.1:8000/api/words/gttsApi/<arg>/
    permission_classes = (permissions.AllowAny,)
    queryset = WordTerm.objects.all()
    serializer = WordTermSerializer(queryset, many=True)

    def get(self, request, word=None):  # get word by url
        queryset = WordTerm.objects.filter(word=word)
        term = slugify(queryset[0])
        language = 'en'

        return Response(
            {'success': "word term"},
            status=status.HTTP_202_ACCEPTED
        )
