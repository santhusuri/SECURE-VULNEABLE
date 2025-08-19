from django.utils.deprecation import MiddlewareMixin

class SimulationSecurityMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        mode = request.session.get('sim_mode', 'secure')
        # Demonstrate cookie/header hardening differences
        if mode == 'secure':
            response.headers.setdefault('X-Content-Type-Options', 'nosniff')
            response.headers.setdefault('X-Frame-Options', 'DENY')
            response.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
            response.headers.setdefault('Permissions-Policy', 'geolocation=(), microphone=()')
        else:
            # Reduce some headers in vulnerable mode (for demo). Do not remove essential ones like session.
            response.headers.pop('X-Frame-Options', None)
        return response