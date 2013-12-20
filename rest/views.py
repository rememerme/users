from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from users.models import User
from users.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pycassa
from django.conf import settings


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class UsersListView(APIView):
    '''
       Used for searching by properties or listing all users available.
    '''
    def get(self, request, format=None):
        pool = pycassa.ConnectionPool('users', server_list=settings.CASSANDRA_NODES)
        userCF = pycassa.ColumnFamily(pool, 'user')
        
        userCF

        pool.dispose()
        return Response(UserSerializer(users, many=True).data)

    '''

    '''
    def post(self, request, format=None):
        pass
