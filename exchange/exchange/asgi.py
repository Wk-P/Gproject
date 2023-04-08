import os
import sys
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.conf import settings
import uwsgi

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gproject.settings')

application = StaticFilesHandler(get_wsgi_application())

uwsgi.set_python_optimize()
uwsgi.add_file_monitor(
    pth=os.path.abspath(__file__),
    callback=lambda *args, **kwargs: sys.exit(0)
)
