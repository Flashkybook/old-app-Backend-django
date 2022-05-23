from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .serializers import UserSerializer

from .models import User


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)  # tuple

    def post(self, request):
        try:
            data = request.data

            # form data
            username = data['username']
            email = data['email']
            password = data['password']
            re_password = data['re_password']

            if password == re_password:
                if len(password) >= 8:
                    if not User.objects.filter(email=email):                        
                        if not User.objects.filter(username=username):
                            user = User.objects.create_user(
                                email=email,
                                username=username,
                                password=password,
                            )
                            user.save()
                            if User.objects.filter(email=email).exists():
                                return Response(
                                    {'success': 'User created', },
                                    status=status.HTTP_201_CREATED
                                )
                            else:
                                return Response(
                                    {'error': 'verify user is fail', },
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                                )
                        else:
                            return Response(
                                {'error': 'User Name Already Exists'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        
                    else:
                        return Response(
                            {'error': 'Email Account Already Exists'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {'error': 'password must be at least 8 characters in length', },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'error': 'password do not match', },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'error 505 algo no funciona correctamente',
                    'data': request.data},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoadUserView(APIView):
    queryset = User.objects.none()

    def get(self, request, format=None):
            try:
                user = UserSerializer(request.user)
                return Response(
                    {'success': user.data},
                    status=status.HTTP_200_OK
                )
            except:
                return Response(
                    {'error': 'error 505 algo no funciona correctamente', },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
  
