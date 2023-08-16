from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.core.exceptions import ObjectDoesNotExist
import sentry_sdk

from datetime import datetime, timedelta

from utils import send_email, get_available_times_for_day

from barbershop.permissions import PermissionBarber
from users.models import UserProfile
from .serializers import CompanysSerializers, SchedulesSerializer, DaysSerializer, SchedulesDaysSerializer
from .models import Company, Schedules, Days, SchedulesDays


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

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def create_business_day(self, request):
        data = request.data
        try:
            data_str = data['start']
            data_obj = datetime.strptime(data_str, '%H:%M')
            data_end = data['end']
            data_str_end = datetime.strptime(data_end, '%H:%M')
            data_pause = data.get('pause_time', None)
            data_end_pause = data.get('end_pause_time', None)

            if data_pause != None and data_end_pause != None:
                data_str_pause = datetime.strptime(data_pause, '%H:%M')
                data_str_end_pause = datetime.strptime(data_end_pause, '%H:%M')
                Days.objects.create(
                    company_id=data['id'],
                    day=data['day'],
                    start=data_obj,
                    end_time=data_str_end,
                    pause_time=data_str_pause,
                    end_pause_time=data_str_end_pause
                )

            Days.objects.create(
                company_id=data['id'],
                day=data['day'],
                start=data_obj,
                end_time=data_str_end
            )
            return Response({'message': 'Dia registrado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao registrar dia!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PATCH'], permission_classes=[PermissionBarber])
    def update_business_day(self, request):
        data = request.data
        try:
            data_str = data['start']
            data_obj = datetime.strptime(data_str, '%H:%M')
            data_end = data['end']
            data_str_end = datetime.strptime(data_end, '%H:%M')
            data_pause = data['pause_time']
            data_str_pause = datetime.strptime(data_pause, '%H:%M')
            data_end_pause = data['end_pause_time']
            data_str_end_pause = datetime.strptime(data_end_pause, '%H:%M')
            day = Days.objects.get(pk=data['day_id'])
            day.company_id = data['company_id']
            day.day = data['day']
            day.start = data_obj
            day.end = data_str_end
            day.pause_time = data_str_pause
            day.end_pause_time = data_str_end_pause
            day.save()
            return Response({'message': 'Dia atualizado com sucesso'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Dia não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao atualizar dia!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list_days(self, request):
        params = request.query_params
        try:
            company_days = Days.objects.filter(company_id=params['company_id'])
            serializer = DaysSerializer(company_days, many=True)
            return Response({'message': 'Sucesso', 'company_days': serializer.data}, status=status.HTTP_200_OK)
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
        try:
            data_str = data['date']
            data_obj = datetime.strptime(data_str, '%d/%m/%Y %H:%M')

            schedules_existing = SchedulesDays.objects.filter(data=data_obj).exists()
            if schedules_existing:
                return Response({'message': 'já existe um agendamento para este horário!'},
                                status=status.HTTP_400_BAD_REQUEST)

            schedule = Schedules.objects.create(
                barbershop_id=data['barbershop_id'],
                client_id=user.id,
                day_id=data['day_id'],
                date=data_obj,
                chosen_barber_id=data['chosen_barber_id'],
                confirmed_by_barber=data['confirmed_by_barber']
            )
            SchedulesDays.objects.create(
                day_id=data['day_id'],
                schedule_id=schedule.id,
                data=data_obj
            )
            date_msg = datetime.strftime(data_obj, '%d/%m/%Y às %H:%M')
            instance = UserProfile.objects.get(pk=data['chosen_barber_id'])
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
            schedule.day_id = data['day_id']
            schedule.date = data_obj
            schedule.chosen_barber_id = data['chosen_barber_id']
            schedule.confirmed_by_barber = data['confirmed_by_barber']
            schedule.save()

            schedule_day = SchedulesDays.objects.filter()
            schedule_day.day_id = data['day_id'],
            schedule_day.schedule_id = schedule.id,
            schedule_day.data = data_obj
            schedule_day.save()

            return Response({'message': 'Agendamento atualizado com sucesso'}, status=status.HTTP_200_OK)
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

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def schedule_by_id(self, request):
        params = request.query_params
        try:
            schedule = Schedules.objects.get(pk=params['schedule_id'])
            serializer = SchedulesSerializer(schedule)
            return Response({'message': 'Agendamento encontrado', 'schedule': serializer.data},
                            status=status.HTTP_200_OK)
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
            return Response({'message': 'Erro ao listar seus agendamentos'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def schedules_days_by_id(self, request):
        params = request.query_params
        try:
            now = datetime.now()
            schedules = SchedulesDays.objects.get(id=params['schedule_day_id'], data__gte=now)
            serializer = SchedulesDaysSerializer(schedules)
            return Response({'message': 'Cortes agendados até o momento', 'schedules': serializer.data})
        except ObjectDoesNotExist:
            return Response({'message': 'Agendamento não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao listar seus agendamentos'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def all_schedules_days(self, request):
        params = request.query_params
        try:
            now = datetime.now()
            schedules = SchedulesDays.objects.filter(
                schedule__barbershop__id=params['company_id']
            ).exclude(data__lt=now).order_by('data')
            serializer = SchedulesDaysSerializer(schedules, many=True)
            return Response({'message': 'Cortes agendados até o momento', 'schedules': serializer.data})
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao listar seus agendamentos'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PATCH'], permission_classes=[PermissionBarber])
    def accept_schedule(self, request):
        data = request.data
        try:
            schedule = Schedules.objects.get(id=data['id'])
            schedule.confirmed_by_barber = data['confirmed_by_barber']
            schedule.save()

            if data['confirmed_by_barber'] == True:
                date_str = datetime.strftime(schedule.date, '%d/%m/%Y às %H:%M')
                subject = 'BarberShop'
                message = f'O barbeiro {schedule.chosen_barber} confirmou o seu agendamento para o dia {date_str}'
                send_email(schedule.client.email, subject, message)
                return Response({'message': 'Agendamento confirmado com sucesso'}, status=status.HTTP_200_OK)
            else:
                date_str = datetime.strftime(schedule.date, '%d/%m/%Y às %H:%M')
                subject = 'BarberShop'
                message = f'O barbeiro {schedule.chosen_barber} infelizmente cancelou seu agendamento para o dia {date_str}'
                send_email(schedule.client.email, subject, message)
                return Response({'message': 'Agendamento cancelado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao confirmar o agendamento'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PUT'], permission_classes=[IsAuthenticated])
    def canceled_by_user(self, request):
        data = request.data
        user = request.user
        try:
            schedule = Schedules.objects.get(pk=data['schedule_id'])
            schedule.user_canceled = data['user_canceled']

            if user != schedule.client:
                return Response({'message': 'Apenas o próprio usuário pode cancelar este agendamento'},
                                status=status.HTTP_401_UNAUTHORIZED)

            if data['user_canceled'] == False:
                return Response({'message': 'Voce não pode fazer está ação, tente remarcar um novo um agendamento'},
                                status=status.HTTP_400_BAD_REQUEST)

            schedule.save()
            return Response({'message': 'Cancelamento feito com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'Response': 'Erro ao cancelar seu agendamento'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def available_times(self, request):
        params = request.query_params
        day_id = params['day_id']
        try:
            day = Days.objects.filter(company__id=day_id).first()

            today = datetime.now()
            end_date = today + timedelta(days=15)

            available_times_today = get_available_times_for_day(day, today)

            available_times_all_days = []
            current_date = today + timedelta(days=1)
            while current_date <= end_date:
                available_times = get_available_times_for_day(day, current_date)
                available_times_all_days.append(
                    {'future_date': current_date.strftime('%Y-%m-%d'), 'times': available_times}
                )
                current_date += timedelta(days=1)

            return Response(
                {
                    'message': 'Horários disponíveis',
                    'available_times_today': available_times_today,
                    'available_times_all_days': available_times_all_days
                },
                status=status.HTTP_200_OK
            )
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao listar horários disponíveis do dia'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
