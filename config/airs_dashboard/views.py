import os
from django.shortcuts import render
from core.logger import AIRS_LOG_FILE
from django.http import JsonResponse

def airs_dashboard(request):
    if os.path.exists(AIRS_LOG_FILE):
        with open(AIRS_LOG_FILE) as f:
            logs = f.readlines()
    else:
        logs = ["No logs yet."]
    
    if request.GET.get('ajax') == '1':
        return JsonResponse({"logs": [log.strip() for log in logs]})
    
    return render(request, "airs_dashboard/airs_dashboard.html", {"logs": logs})
