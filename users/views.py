from django.shortcuts import render
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

from users.models import UserProfile
from users.serializers import UserSerializer


class UserViewset(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False, permission_classes=[AllowAny])
    def register_user(self, request):
        data = request.data
        try:
            email = data['email']

            if UserProfile.objects.filter(email__iexact=email):
                return Response({'message': 'Um usuário com este email já existe.'}, status=status.HTTP_409_CONFLICT)

            first_name = data['full_name'].split(' ', 1)[0]

            user = UserProfile.objects.create(
                username=first_name,
                full_name=data['full_name'],
                email=data['email'],
                token_google=data['token_google']
            )

            user.set_password(data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'message': 'Usuário Cadastrado.'}, status=status.HTTP_200_OK)
            # return Response({'msg': 'Usuário Cadastrado.', 'token': user.auth_token.key, 'user': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            # sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro no cadastro de usuário.', 'error': str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['DELETE'], permission_classes=[IsAuthenticated])
    def delete_user(self, request):
        data = request.data
        try:
            user = UserProfile.objects.get(id=request.user.id)
            user.delete()
            return Response({'message': 'Sucesso Apagado!'},
                            status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return Response({'message': 'Usuario Nao Existente.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as error:
            return Response({'message': 'Nao Foi Possivel Deletar usuario, Entre em Contato com o Suporte.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def update_user(self, request):
        user = request.user
        data = request.data
        try:
            user.full_name = data['full_name']
            user.email = data['email']
            names = user.full_name.split(' ', 1)[0]
            user.first_name = names[0]
            user.last_name = names[1] if len(names) > 1 else ' '
            user.save()
            return Response({'message': 'Dados alterados com sucesso!'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao atualizar o usuário!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def get_user(self, request):
        user = request.user
        try:
            user = UserProfile.objects.get(id=user.id)
            serializer = UserSerializer(user)
            return Response({'message': 'Usuário encontrado', 'user': serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': 'Nao Foi Possivel Deletar usuario, Entre em Contato com o Suporte.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def list_users(self, request):
        try:
            user = UserProfile.objects.all()
            serializer = UserSerializer(user, many=True)
            return Response({'message': 'Usuários encontrados', 'user': serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': 'Nao Foi Possivel Deletar usuario, Entre em Contato com o Suporte.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)