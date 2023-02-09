from rest_framework import serializers
from .models import Account

# for user json details provider
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        exclude=['password']
        
 # adding some data into jwt token 
class AccountSerializerWithToken(AccountSerializer):
       class Meta:
        model=Account
        fields=['id','email','name','is_admin']


