# app/apps.py

from django.apps import AppConfig

class AppConfig(AppConfig):
  name = 'myapp'

  def ready(self):
      import myapp.tasks  # Import tasks to ensure they are registered