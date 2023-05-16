from django.shortcuts import render
from .models import Company

class GasDistributorViewSet(viewsets.ModelViewSet):

    @action(methods=['POST'], detail=False, permission_classes=[AllowAny])
    def register_company(self, request):
        data = request.data
        try:
            company = Company.objects.create(
                name = data['name'],
                phone = data['phone'],
                cep = data['cep'],
                city = data['city'],
                neighborhood = data['neighborhood'],
                state = data['state'],
                street = data['cep'],
                instagram_link = data['instagram_link'],
                facebook_link = data['facebook_link'],
                business_hours = data['business_hours']
        
            )
            return Response({'message': 'Barbearia Cadastrada.'}, status=status.HTTP_200_OK)
            # return Response({'msg': 'Usuário Cadastrado.', 'token': user.auth_token.key, 'user': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            #sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro no cadastro de usuário.', 'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
