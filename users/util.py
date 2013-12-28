'''
    Gets the offset and limit parameters from the request with the
    proper offset and limit settings.

    Created on Dec 20, 2013

    @author: Andrew Oberlin
'''

from django.conf import settings
from rest_framework.exceptions import APIException
from django.db import models
import hashlib

'''
    Gets the correct value for the offset and limit based on the application
    settings.
    
    @param request: The request being made to the server
'''
def getLimit(request):
    limit = settings.REST_FRAMEWORK.PAGINATE_BY
    
    # gets the limit of the request and defaults to the maximum if the limit passed is too big
    # also if no limit is sent then the limit in the settings is used
    if 'limit' in request.QUERY_PARAMS:
        maxLimit = settings.REST_FRAMEWORK.MAX_PAGINATE_BY
        limit = maxLimit if request.QUERY_PARAMS['limit'] > maxLimit else request.QUERY_PARAMS['limit']
    
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
        Overriding the default delete method to remove Django operation.
        
        This delete will do nothing and will not be used.
    '''
    def delete(self):
        pass
    
    class Meta:
        app_label = u'users'

'''
    Bad Request Exception.
'''
class BadRequestException(APIException):
    status_code = 400
    detail = "A Bad Request was made for the API. Revise input parameters."
    
'''

'''
class UserConflictException(APIException):
    status_code = 409
    detail = "The user requested for creation already exists"