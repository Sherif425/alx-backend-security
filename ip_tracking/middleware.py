import logging
from ipware import get_client_ip
from .models import RequestLog

logger = logging.getLogger(__name__)

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)
        if ip:
            RequestLog.objects.create(ip_address=ip, path=request.path)
            logger.info(f"Logged IP: {ip} | Path: {request.path}")
        return self.get_response(request)
