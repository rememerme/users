from models import User
from rest_framework import serializers

'''
    The User serializer used to display a model to the web through json serialization.
'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'username', 'email')
        
'''
    The User serializer used to create a python dictionary for submitting to the
    Cassandra database with the correct options.
'''
class CassaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'salt', 'password', 'active', 'facebook', 'premium')