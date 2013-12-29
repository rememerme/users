from rest_framework.exceptions import APIException

'''
    Bad Request Exception.
'''
class BadRequestException(APIException):
    status_code = 400
    detail = "A Bad Request was made for the API. Revise input parameters."

'''

'''
class UserAuthorizationException(APIException):
    status_code = 401
    detail = "Incorrect password user password combination"
    
'''

'''
class UserConflictException(APIException):
    status_code = 409
    detail = "The user requested for creation already exists"
    
'''

'''
class UserNotFoundException(APIException):
    status_code = 400
    detail = "The user requested does not exist"