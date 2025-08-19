from functools import wraps

def mode_switch(secure_impl, vulnerable_impl):
    @wraps(secure_impl)
    def _wrapped(request, *args, **kwargs):
        mode = request.session.get('sim_mode', 'secure')
        if mode == 'vulnerable':
            return vulnerable_impl(request, *args, **kwargs)
        return secure_impl(request, *args, **kwargs)
    return _wrapped