from django.shortcuts import render
from rest_framework import viewsets
from .serializer import AccountSerializer, AccountSerializerWithToken
from .models import Account
from rest_framework.permissions import  IsAdminUser
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework  import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# customizing and adding data to jwt token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)     
        serializer=AccountSerializerWithToken(self.user).data
        for k ,v in serializer.items():
            data[k]=v
        return data
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)    
        token['admin'] = user.is_admin 
        return token
    
# for simple jwt customization
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# admin register   view
@api_view(['POST'])
def user_register(request):
    try:
        data=request.data
        name=data['name']
        email=data['email']
        password=data['password']
        confirm_password=data['confirm_password']

        # validatations for blank
        if email=='' or name=='' or name ==''  or password=='' or confirm_password=='':
            message={'error':' fill the blanks'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        # validation for password matching
        elif password!=confirm_password:
            message={'error':'password missmatch'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        # for password length check
        elif len(password)<6:
            message={'error':'password contain min 6 charector'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        
        # checking the email is already exist or not
        elif Account.objects.filter(email=email).exists():
            message={'error':'This email is already exist'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
            
        # creating a object of Account model for signup 
        user=Account.objects.create(
            name=name,
            email=email,
            password=make_password(password),
             
        )
        serializere=AccountSerializer(user,many=False)
        return Response(serializere.data)
    except:
        message={'error':'there is a error occure'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)    
 
 
# update and view users   
class userDetails(viewsets.ModelViewSet):
    permission_classes=[IsAdminUser]
    queryset=Account.objects.filter(is_admin=False)
    serializer_class=AccountSerializer

