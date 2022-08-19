from django.db import models
from django.utils import timezone


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)


    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)


    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


    def get_duration(self):
        if self.leaved_at:
            time_in_storage = self.leaved_at - self.entered_at
        else:
            time_in_storage = timezone.now() - self.entered_at
        seconds_in_storage = time_in_storage.total_seconds()
        return seconds_in_storage

 
    def is_visit_long(self, minutes=60):
        seconds_in_storage = self.get_duration()
        return (seconds_in_storage / 60) > minutes


def format_duration(duration):
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)    
    seconds = int((duration % 3600) % 60)
    return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
