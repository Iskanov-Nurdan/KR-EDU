from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse


class RateLimitMiddleware:
    """Per-IP request throttling using a fixed-window counter in cache.

    Mitigates brute-force attempts against /admin/login/ and basic
    single-source flooding. It cannot stop distributed/volumetric DDoS —
    that requires protection at the network edge (Cloudflare, ngrok, a
    reverse proxy with rate limiting, etc.).
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.general_limit, self.general_window = getattr(
            settings, 'RATELIMIT_GENERAL', (120, 60)
        )
        self.strict_limit, self.strict_window = getattr(
            settings, 'RATELIMIT_STRICT', (10, 60)
        )
        self.strict_paths = getattr(settings, 'RATELIMIT_STRICT_PATHS', ())

    def _client_ip(self, request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')

    def __call__(self, request):
        ip = self._client_ip(request)
        is_strict = request.path in self.strict_paths
        limit = self.strict_limit if is_strict else self.general_limit
        window = self.strict_window if is_strict else self.general_window
        key = f'ratelimit:{"strict" if is_strict else "general"}:{ip}'

        count = cache.get(key, 0)
        if count >= limit:
            return HttpResponse(
                'Слишком много запросов. Попробуйте позже.',
                status=429,
                content_type='text/plain; charset=utf-8',
            )
        cache.add(key, 0, window)
        try:
            cache.incr(key)
        except ValueError:
            cache.set(key, 1, window)

        return self.get_response(request)
