from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializers import UserBookSerializer, WordTermSerializer
from .models import UserBook, WordTerm

# Create your views here.


class ViewUserBook(APIView):
    # solo pueden acceeder usuarion que manden token JWT
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
                    {'error': "error 505 algo no funciona correctamente", },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:

            return Response(
                {'error': "No allow POST method ", },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# View Dictionary GET

# add Term http://127.0.0.1:8000/api/words/add_to_dict/


class AddWordTerms(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        """POST, crea un nuevo objeto WordTerm y lo agrega al userbook del current user
        si este ya existe entonces lo encontramos y lo agregamos al current user book """
        # queryset = Dictionary.objects.filter(user=request.user.id)
        try:
            data = request.data
            word_exist = WordTerm.objects.filter(word=data).exists()
            is_phrase = False
            if len(data.split()) > 1:
                is_phrase = True
            # created and added
            if not word_exist:  # si no existe crea el termino y lo agrega a userbook
                word = WordTerm.objects.create(word=data, phrase=is_phrase)
                word.save()
                # Lo agrega al user book
                user_book = UserBook.objects.create(
                    user=request.user, terms=word)
                user_book.save()
                return Response(
                    {'success': "word add to dictionary and add to user book"},
                    status=status.HTTP_201_CREATED
                )
            # term exist only add
            else:
                word = WordTerm.objects.get(word=data)
                user_book_exist = UserBook.objects.filter(
                    user=request.user, terms=word)
                if not user_book_exist:
                    # Lo agrega al user book
                    user_book = UserBook.objects.create(
                        user=request.user, terms=word)
                    user_book.save()
                    return Response(
                        {'success': "word add to user book"},
                        status=status.HTTP_202_ACCEPTED
                    )

                else:
                    return Response(
                        {'error': "error 505 already exist in your userbook"},
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
        except:
            print("error 401 error de peticion try")
            return Response(
                {'error': "error 505 neither added or created"},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

# https://github.com/alankan886/SuperMemo2
from supermemo2 import SMTwo
import datetime
class StudyWordSession(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        data = request.data
        queryset = UserBook.objects.get(id=data['id'])

        # user = request.user
        # serializer = UserBookSerializer(queryset, many=True)

        today = datetime.date.today() # only day


        # PRIMERA VES QUE SE ESTUDIA LA PALABRA
        if queryset.last_review == None :
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
                review = SMTwo(queryset.easiness, queryset.interval, queryset.repetitions).review(data['easiness'])
                queryset.easiness = review.easiness
                queryset.interval = review.interval
                queryset.repetitions = review.repetitions
                queryset.next_review_date = review.review_date
            
        
        queryset.last_review = today

        queryset.save()
        # print(queryset, "easiness:",queryset.easiness, "interval:",queryset.interval,"repetitions:", queryset.repetitions, "next_review_date:",queryset.next_review_date, "last_review:",queryset.last_review, "===", today )

        try:
            return Response(
                {"success": "study session update"},
                status=status.HTTP_202_ACCEPTED
            )
        except:
            print("error 401 error de peticion try")
            return Response(
                {'error': "error 505 neither added or created"},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )