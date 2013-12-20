from django.db import models
import pycassa

# User model faked to use Cassandra

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    premium = models.BooleanField()
    email = models.TextField()
    username = models.TextField()
    facebook = models.BooleanField()

    class Meta:
        app_label = u'users'
