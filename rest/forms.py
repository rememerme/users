'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for users.
    
    Created on Dec 20, 2013

    @author: Andrew Oberlin
'''
from django import forms
from users.util import getOffsetLimit

from models import User

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
        