"""
WSGI config for users project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/virtualenv/django-cassa-env/local/lib/python2.7/site-packages')

# Add the projevct onto the syspath
sys.path.append('/env/users')
sys.path.append('/env/users/users')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "users.settings")

# Activate teh users-env virtual env
activate_env=os.path.expanduser("/virtualenv/django-cassa-env/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
