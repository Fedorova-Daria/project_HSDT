from django.core.management.base import BaseCommand
from requests.models import TeamJoinRequest
from django.utils.timezone import now
from datetime import timedelta

class Command(BaseCommand):
    help = "Удаляет заявки, которые старше 7 дней"

    def handle(self, *args, **kwargs):
        expired_requests = TeamJoinRequest.objects.filter(created_at__lt=now() - timedelta(days=7))
        count = expired_requests.count()
        expired_requests.delete()
        self.stdout.write(self.style.SUCCESS(f"Удалено {count} устаревших заявок."))

