from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.core.exceptions import ObjectDoesNotExist
import sentry_sdk

from datetime import datetime

from utils import send_email

from barbershop.permissions import PermissionBarber
from users.models import UserProfile
from .serializers import CompanysSerializers, SchedulesSerializer
from .models import Company, Schedules


class CompanysViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanysSerializers
    permission_classes = [IsAuthenticated]

    @action(methods=['POST'], detail=False, permission_classes=[AllowAny])
    def register_company(self, request):
        user = request.user
        data = request.data
        try:
            business_hours_array = data['business_hours']
            business_hours = []
            for business_hour in business_hours_array:
                business_hours.append(business_hour)

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
                business_hours=business_hours
            )
            company.owner.add(user.id)
            return Response({'message': 'Barbearia Cadastrada.'}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro no cadastro de usuário.', 'error': str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def update_company(self, request):
        user = request.user
        data = request.data
        try:
            business_hours_array = data['business_hours']
            business_hours = []
            for business_hour in business_hours_array:
                business_hours.append(business_hour)

            company = Company.objects.get(id=data['company_id'])
            company.name = data['name']
            company.phone = data['phone']
            company.cep = data['cep']
            company.city = data['city']
            company.neighborhood = data['neighborhood']
            company.state = data['state']
            company.street = data['cep']
            company.instagram_link = data['instagram_link']
            company.facebook_link = data['facebook_link']
            company.business_hours = business_hours
            company.save()

            return Response({'message': 'Barbearia atualizada com sucesso.'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Barbearia não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro no cadastro de usuário.', 'error': str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def list_all_companys(self, request):
        try:
            companys = Company.objects.all()
            serializer = CompanysSerializers(companys, many=True)
            return Response({'message': 'Sucesso', 'companys': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao listar barbearia(s)'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def companys_by_user(self, request):
        user = request.user
        try:
            companys_user = Company.objects.filter(owner=user)
            serializer = CompanysSerializers(companys_user, many=True)
            return Response({'message': 'Sucesso', 'companys_user': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao buscar barbearia(s)'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def companys_by_id(self, request):
        params = request.query_params
        try:
            companys_user = Company.objects.get(id=params['company_id'])
            serializer = CompanysSerializers(companys_user)
            return Response({'message': 'Sucesso', 'companys_user': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Barbearia não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao buscar por barbearia'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SchedulesViewset(ModelViewSet):
    queryset = Schedules.objects.all()
    serializer_class = SchedulesSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def schedule_cut(self, request):
        user = request.user
        data = request.data
        barber_id = data['chosen_barber_id']
        try:
            data_str = data['date']
            data_obj = datetime.strptime(data_str, '%d/%m/%Y %H:%M')
            Schedules.objects.create(
                client_id=user.id,
                date=data_obj,
                chosen_barber_id=barber_id,
                confirmed_by_barber=data['confirmed_by_barber']
            )

            date_msg = datetime.strftime(data_obj, '%d/%m/%Y às %H:%M')
            instance = UserProfile.objects.get(pk=barber_id)
            subject = 'BarberShop'
            message = f'O cliente {user} fez um novo agendamento para o dia {date_msg}'
            send_email(instance.email, subject, message)

            return Response({'message': 'Agendamento feito com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao marcar agendamento'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def update_schedule_cut(self, request):
        user = request.user
        data = request.data
        try:
            data_str = data['date']
            data_obj = datetime.strptime(data_str, '%d/%m/%Y %H:%M')
            schedule = Schedules.objects.get(id=data['schedule_id'])
            schedule.client_id = user.id
            schedule.date = data_obj
            schedule.chosen_barber_id = data['chosen_barber_id']
            schedule.confirmed_by_barber = data['confirmed_by_barber']
            schedule.save()
            return Response({'message': 'Agendamento feito com sucesso'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Barbearia encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao marcar agendamento'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def list_all_schedules(self, request):
        try:
            now = datetime.now()
            schedules = Schedules.objects.all().exclude(date__lt=now)
            serializer = SchedulesSerializer(schedules, many=True)
            return Response({'message': 'Sucesso', 'schedules': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao listar agendamentos'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[PermissionBarber])
    def schedule_by_id(self, request):
        params = request.query_params
        try:
            now = datetime.now()
            schedule = Schedules.objects.get(pk=params['schedule_id']).exclued(date__lt=now)
            serializer = SchedulesSerializer(schedule)
            return Response({'message': 'Agendamento encontrado', 'schedule': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Agendamento não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao listar agendamento'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def schedule_by_user(self, request):
        user = request.user
        try:
            now = datetime.now()
            schedules = Schedules.objects.filter(chosen_barber_id=user.id).exclude(date__lt=now)
            serializer = SchedulesSerializer(schedules, many=True)
            return Response({'message': 'Cortes agendados para você', 'schedules': serializer.data})
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao listar seus agendamentos'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PATCH'], permission_classes=[PermissionBarber])
    def accept_schedule(self, request):
        data = request.data
        try:
            schedule = Schedules.objects.get(id=data['id'])
            schedule.confirmed_by_barber = data['confirmed_by_barber']
            schedule.save()
            return Response({'message': 'Agendamento confirmado/cancelado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao confirmar o agendamento'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)