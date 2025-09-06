from django.core.cache import cache
from django_ip_geolocation.geolocation import IpGeoLocation

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)
        country, city = None, None

        if ip:
            # Check cache first
            cached_geo = cache.get(f"geo:{ip}")
            if cached_geo:
                country, city = cached_geo
            else:
                try:
                    geo = IpGeoLocation(ip)
                    country = geo.country_name
                    city = geo.city
                    cache.set(f"geo:{ip}", (country, city), 86400)  # Cache for 24h
                except Exception:
                    pass

            RequestLog.objects.create(ip_address=ip, path=request.path,
                                      country=country, city=city)

        return self.get_response(request)
