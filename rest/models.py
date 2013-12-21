from users.util import CassaModel
from django.db import models
import pycassa
from django.conf import settings
import uuid

# User model faked to use Cassandra
POOL = pycassa.ConnectionPool('users', server_list=settings.CASSANDRA_NODES)

class User(CassaModel):
    user_id = models.IntegerField(primary_key=True)
    premium = models.BooleanField()
    email = models.TextField()
    username = models.TextField()
    facebook = models.BooleanField()
    '''
        Gets the user given an ID.
        
        @param user_id: The uuid of the user.
    '''
    @staticmethod
    def getByID(user_id):
        pass
    
    '''
        Gets the user given a username.
        
        @param username: The username of the user.
    '''
    @staticmethod
    def getByUsername(username):
        pass
    
    '''
        Gets the user by the email.
        
        @param email: The email of the user.
    '''
    @staticmethod
    def getByEmail(email):
        pass
    
    '''
        Gets all of the users and uses an offset and limit if
        supplied.
        
        @param offset: Optional argument. Used to offset the query by so
            many entries.
        @param limit: Optional argument. Used to limit the number of entries
            returned by the query.
    '''
    @staticmethod
    def all(offset=None, limit=None):
        pass
    
    '''
        Saves a set of users given by the cassandra in/output, which is
        a dictionary of values.
        
        @param users: The set of users to save to the user store.  
    '''
    @staticmethod
    def save(users):
        if not isinstance(users,list):
            users = [users]

        for user in users:
            table = pycassa.ColumnFamily(POOL, 'user')
            new_user = uuid.uuid1()
            table.insert(new_user, user)

    
    
    