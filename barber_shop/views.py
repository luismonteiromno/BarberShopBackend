from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
import sentry_sdk

from .serializers import CompanysSerializers
from .models import Company


class CompanysViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanysSerializers
    permission_classes = [IsAuthenticated]

    @action(methods=['POST'], detail=False, permission_classes=[AllowAny])
    def register_company(self, request):
        data = request.data
        try:
            company = Company.objects.create(
                name=data['name'],
                phone=data['phone'],
                cep=data['cep'],
                city=data['city'],
                neighborhood=data['neighborhood'],
                state=data['state'],
                street=data['cep'],
                instagram_link=data['instagram_link'],
                facebook_link=data['facebook_link'],
                business_hours=data['business_hours']
        
            )
            return Response({'message': 'Barbearia Cadastrada.'}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro no cadastro de usuário.', 'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def list_all_companys(self, request):
        try:
            companys = Company.objects.all()
            serializer = CompanysSerializers(companys, many=True)
            return Response({'message': 'Sucesso', 'companys': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def companys_by_user(self, request):
        user = request.user
        try:
            companys_user = Company.objects.filter(owner=user)
            serializer = CompanysSerializers(companys_user, many=True)
            return Response({'message': 'Sucesso', 'companys_user': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)