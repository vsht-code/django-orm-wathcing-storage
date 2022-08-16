from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone

def format_duration(duration):
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)    
    seconds = int((duration % 3600) % 60)
    return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)



def storage_information_view(request):

    # Программируем здесь
    visits = Visit.objects.filter(leaved_at=None)
    for visit in visits:
        non_closed_visits = [
            {
                'who_entered': visit.passcard.owner_name,
                'entered_at': timezone.localtime(visit.entered_at),
                'duration': format_duration(visit.get_duration()),
            }
        ]
        context = {
            'non_closed_visits': non_closed_visits,  # не закрытые посещения
        }
        return render(request, 'storage_information.html', context)
