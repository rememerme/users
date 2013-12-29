'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for users.
    
    Created on Dec 20, 2013

    @author: Andrew Oberlin
'''
from django import forms
from users.util import getLimit
import bcrypt
from models import User
from users import util
from rest.exceptions import UserConflictException, UserNotFoundException, BadRequestException
from rest.serializers import UserSerializer
from uuid import UUID
from pycassa.cassandra.ttypes import NotFoundException as CassaNotFoundException

class UserPostForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    premium = forms.BooleanField(required=False)
    facebook = forms.BooleanField(required=False)
    active = forms.BooleanField(required=False)

    '''
        Overriding the clean method to add the default offset and limiting information.
    '''
    def clean(self):
        self.cleaned_data['premium'] = self.cleaned_data['premium'] if 'premium' in self.cleaned_data else False
        self.cleaned_data['active'] = self.cleaned_data['active'] if 'active' in self.cleaned_data else True
        self.cleaned_data['facebook'] = self.cleaned_data['facebook'] if 'facebook' in self.cleaned_data else False
        self.cleaned_data['salt'] = bcrypt.gensalt()
        self.cleaned_data['password'] = util.hash_password(self.cleaned_data['password'], self.cleaned_data['salt'])
        return self.cleaned_data
    
    '''
        Submits this form to retrieve the correct information requested by the user.
        Defaults to search by username. Then, will check if the email parameter is
        provided.
        
        This means a query with email and username both set will ignore username.
        
        @return: A list of users matching the query with the given offset/limit
    '''
    def submit(self):
        user = User.fromMap(self.cleaned_data)
        # check if username and email have not been used yet
        # if they have not then save the user
        if User.getByEmail(user.email) or User.getByUsername(user.username):
            raise UserConflictException()
        
        user.save()
        return user
        
class UserGetListForm(forms.Form):
    page = forms.CharField(required=False)
    limit = forms.IntegerField(required=False)
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    '''
        Overriding the clean method to add the default offset and limiting information.
    '''
    def clean(self):
        self.cleaned_data['limit'] = getLimit(self.cleaned_data)
        self.cleaned_data['page'] = None if not self.cleaned_data['page'] else self.cleaned_data['page']
        # remove the parameters from the cleaned data if they are empty
        if not self.cleaned_data['username']:
            del self.cleaned_data['username']
            
        if not self.cleaned_data['email']:
            del self.cleaned_data['email']
        
        return self.cleaned_data
    
    '''
        Submits this form to retrieve the correct information requested by the user.
        Defaults to search by username. Then, will check if the email parameter is
        provided.
        
        This means a query with email and username both set will ignore username.
        
        @return: A list of users matching the query with the given offset/limit
    '''
    def submit(self):
        if 'username' in self.cleaned_data:
            ans = User.getByUsername(self.cleaned_data['username'])
            uResponse = UserSerializer([] if not ans else [ans], many=True).data
            response = { 'data' : uResponse }
            return response
        elif 'email' in self.cleaned_data:
            ans = User.getByEmail(self.cleaned_data['email'])
            uResponse = UserSerializer([] if not ans else [ans], many=True).data
            response = { 'data' : uResponse }
            return response
        else:
            ans = User.all(page=self.cleaned_data['page'], limit=self.cleaned_data['limit'])
            uResponse = UserSerializer(ans, many=True).data
            response = { 'data' : uResponse }
            if ans:
                response['next'] = ans[-1].user_id
            return response
        
class UserGetSingleForm(forms.Form):
    user_id = forms.CharField(required=True)
    
    
    def clean(self):
        try:
            self.cleaned_data['user_id'] = UUID(self.cleaned_data['user_id'])
            return self.cleaned_data
        except ValueError:
            raise BadRequestException()
    
    '''
        Submits a form to retrieve a user given the user_id.
        
        @return: A user with the given user_id
    '''
    def submit(self):
        try:
            ans = User.getByID(self.cleaned_data['user_id'])
            if not ans:
                raise UserNotFoundException()
        except CassaNotFoundException:
            raise UserNotFoundException()
        return UserSerializer(ans).data
        