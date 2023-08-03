from account import serializers
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from account.services import RegistrationMixin
from django.conf import settings
import requests





class UserCreateView(RegistrationMixin):
    serializer_class = serializers.UserRegisterSerializer


    def create(self, request, *args, **kwargs):
        url = 'https://www.google.com/recaptcha/api/siteverify'
        params = {
            "secret": settings.RECAPTCHA_PRIVATE_KEY,
            "response": self.serializer_class.validated_data.get('grecaptcha_token')
        }
        try:
            serializer =self.serializer_class(request.data)
            response = requests.post(url, params=params)
            data = response.json()
            if data.get("success") is False:
                return Response({
                    "message": "Google Recaptcha не пройдена"
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': f'{e}'}, status=status.HTTP_403_FORBIDDEN)



 

       
        


   

    

