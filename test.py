from django.conf import settings
settings.configure(CASSANDRA_NODES = ('134.53.148.102',))
from users.models import User
User.save('Andy')

