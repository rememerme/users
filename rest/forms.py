'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for users.
    
    Created on Dec 20, 2013

    @author: Andrew Oberlin
'''
from django import forms
from users.util import getOffsetLimit
import bcrypt
from models import User
from users import util
from users.util import UserConflictException

class UserPutForm(forms.Form):
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
    offset = forms.IntegerField(required=False)
    limit = forms.IntegerField(required=False)
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    '''
        Overriding the clean method to add the default offset and limiting information.
    '''
    def clean(self):
        self.cleaned_data['offset'], self.cleaned_data['limit'] = getOffsetLimit(self.cleaned_data)
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
            return [User.getByUsername(self.cleaned_data['username'])]
        elif 'email' in self.cleaned_data:
            return [User.getByEmail(self.cleaned_data['email'])]
        else:
            return User.all(offset=self.cleaned_data['offset'], limit=self.cleaned_data['limit'])
        