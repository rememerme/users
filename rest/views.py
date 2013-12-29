from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pycassa
from django.conf import settings
from rest.forms import UserGetListForm, UserPostForm, UserGetSingleForm
from rest.exceptions import BadRequestException

class UsersListView(APIView):
    '''
       Used for searching by properties or listing all users available.
       Also, used to create new users.
    '''
    
    def get(self, request):
        '''
            Used to search users by username or email.
        '''
        # get the offset and limit query parameters
        form = UserGetListForm(request.QUERY_PARAMS)
        
        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()
            

    def post(self, request):
        '''
            Used to create a new user.
        '''
        form = UserPostForm(request.DATA)

        if form.is_valid():
            return Response(UserSerializer(form.submit()).data)
        else:
            raise BadRequestException()
        
class UsersSingleView(APIView):
    '''
       Used for managing user properties, getting specific users and deleting users.
    '''
    
    def get(self, request, user_id):
        '''
            Used to get a user by id.
        '''
        # get the offset and limit query parameters
        request.DATA['user_id'] = user_id
        form = UserGetSingleForm(request.DATA)
        
        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()
            
    '''
    def put(self, request):
        form = UserPostForm(request.DATA)

        if form.is_valid():
            return Response(UserSerializer(form.submit()).data)
        else:
            raise BadRequestException()
    '''
    
