'''
    Gets the offset and limit parameters from the request with the
    proper offset and limit settings.

    Created on Dec 20, 2013

    @author: Andrew Oberlin
'''

from django.conf import settings
from django.db import models
import hashlib

'''
    Gets the correct value for the offset and limit based on the application
    settings.
    
    @param request: The request being made to the server
'''
def getLimit(request):
    limit = settings.REST_FRAMEWORK['PAGINATE_BY']
    
    # gets the limit of the request and defaults to the maximum if the limit passed is too big
    # also if no limit is sent then the limit in the settings is used
    if 'limit' in request and request['limit']:
        maxLimit = settings.REST_FRAMEWORK['MAX_PAGINATE_BY']
        limit = maxLimit if request['limit'] > maxLimit else request['limit']
    
    return limit

'''
    Hashes a password with the given salt. If no salt is provided, the salt that will be
    used is an empty string.
'''
def hash_password(password, salt=''):
    password = password.encode('utf8') if isinstance(password, unicode) else password
    salt = salt.encode('utf8') if isinstance(salt, unicode) else salt
    
    return unicode(hashlib.sha256(salt + password).hexdigest())

'''
    Model that we can use to get rid of the Django stuff, but still use the model
    concept while coding.
'''
class CassaModel(models.Model):
    '''
        Overriding the default save method to remove Django operation.
        
        This save will do nothing and will not be used.
    '''
    def save(self):
        pass
    
    '''
        Updates this user with the values put into the map.
        
        @param other: The map of values to use for updating the model.
    '''
    def update(self, other):
        for attrKey in self.__dict__.keys():
            if attrKey in other:
                setattr(self, attrKey, other[attrKey])
    
    '''
        Overriding the default delete method to remove Django operation.
        
        This delete will do nothing and will not be used.
    '''
    def delete(self):
        pass
    
    class Meta:
        app_label = u'users'