from django.contrib import messages
from user_agents import parse
from django.utils import timezone
from .models import SessionHistory
import requests
import json
 
def checkIp(request): 
    if request.user.is_staff:
        ip = request.META['REMOTE_ADDR']
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        data = json.loads(response.text)
        if 'error' in data:
            country = 'Unknown'
        else:
            country = data["country_name"]
        
        user_agent = parse(request.META.get('HTTP_USER_AGENT'))
        browser = user_agent.browser.family
        
        sessions = SessionHistory.objects.all()
        if not sessions:
            info = SessionHistory(
                browser=browser, 
                ip=ip, 
                country=country
            )
            info.save()
        
        #Diverso dal ip precedente
        lastIp = sessions.order_by('-date').values('ip')
        if ip != lastIp[0].get('ip'):
            messages.warning(request, "L'indirizzo IP è diverso quello usato in precedenza")

        #Controllo se ip esiste già 
        for dbIp in SessionHistory.objects.values_list('ip'):     
            if ip in dbIp:
                info = SessionHistory.objects.filter(ip=ip).first()
                info.date = str(timezone.now())
                info.save()
                break
        else:
            info = SessionHistory(
                    browser=browser, 
                    ip=ip, 
                    country=country
                )
            info.save()
        return sessions