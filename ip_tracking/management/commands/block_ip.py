from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = "Block an IP address"

    def add_arguments(self, parser):
        parser.add_argument("ip", type=str, help="IP address to block")
        parser.add_argument("--reason", type=str, default="Manual block")

    def handle(self, *args, **kwargs):
        ip = kwargs["ip"]
        reason = kwargs["reason"]
        BlockedIP.objects.get_or_create(ip_address=ip, defaults={"reason": reason})
        self.stdout.write(self.style.SUCCESS(f"Blocked IP: {ip}"))


