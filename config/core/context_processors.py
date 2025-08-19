def simulation_mode(request):
    mode = request.session.get('sim_mode')
    if not mode:
        # use project default
        from django.conf import settings
        mode = settings.SIMULATION_MODE
        request.session['sim_mode'] = mode
    return {'SIM_MODE': mode}