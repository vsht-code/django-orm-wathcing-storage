from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import format_duration
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils import timezone



def passcard_info_view(request, passcode):
    #passcard = Passcard.objects.get(passcode=passcode)
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits_by_passcard = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    for visit in visits_by_passcard:
        this_passcard_visit = {
                'entered_at': timezone.localtime(visit.entered_at),
                'duration': format_duration(visit.get_duration()),
                'is_strange': visit.is_visit_long()
            }
        this_passcard_visits.append(this_passcard_visit)
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
