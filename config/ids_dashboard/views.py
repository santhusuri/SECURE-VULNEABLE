import os
from django.shortcuts import render
from core.logger import IDS_LOG_FILE
from django.http import JsonResponse

def ids_dashboard(request):
    if os.path.exists(IDS_LOG_FILE):
        with open(IDS_LOG_FILE) as f:
            logs = f.readlines()
    else:
        logs = ["No logs yet."]
    
    if request.GET.get('ajax') == '1':
        return JsonResponse({"logs": [log.strip() for log in logs]})
    
    return render(request, "ids_dashboard/ids_dashboard.html", {"logs": logs})
