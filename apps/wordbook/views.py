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
