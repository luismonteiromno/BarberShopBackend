import sentry_sdk
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from .models import AbousUs
from .serializers import AboutUsSerializer


class AboutUsViewSet(ModelViewSet):
    queryset = AbousUs.objects.all()
    serializer_class = AboutUsSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def about_us(self, request):
        try:
            about_us = AbousUs.objects.last()
            if about_us != None:
                serializer = AboutUsSerializer(about_us)
                return Response({'message': 'Sucesso', 'about_us': serializer.data}, status.HTTP_200_OK)
            else:
                return Response({'Nenhuma informação encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)