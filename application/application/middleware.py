from django.http import Http404


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/health-debug-check-1realiz@/':
            u = request.user
            if u.is_anonymous == True or u.is_superuser == False:
                raise Http404
        return self.get_response(request)


class DenyAdminFromApiRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        admin_paths = [
            '/',
            '/admin/',
            '/admin/login/',
        ]

        try:
            subdomain = request.META['HTTP_HOST'].split('.')[0]
        except:
            subdomain = ""

        is_admin_request = False
        for ap in admin_paths:
            if ap == request.path:
                is_admin_request = True

        if is_admin_request and subdomain == "api":
            raise Http404

        return self.get_response(request)
