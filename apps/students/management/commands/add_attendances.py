from django.core.management.base import BaseCommand
from datetime import date, time, timedelta
from models import Lesson, Group  # Update with your actual app name


class Command(BaseCommand):
    help = "Create attendances to lessons"

    def handle(self, *args, **options):
        pass