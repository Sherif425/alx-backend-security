from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_suspicious_ips():
    one_hour_ago = timezone.now() - timedelta(hours=1)
    logs = (RequestLog.objects
            .filter(timestamp__gte=one_hour_ago)
            .values("ip_address")
            .annotate(count=models.Count("id")))

    for log in logs:
        ip = log["ip_address"]
        count = log["count"]

        # Flag IPs making too many requests
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={"reason": f"High traffic: {count} requests in the last hour"}
            )
