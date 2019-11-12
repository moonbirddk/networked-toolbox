from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
# Create your models here.


class EventWorkshop(models.Model): 

    class Meta: 
        verbose_name = "Event Or Workshop"
        verbose_name_plural = "Events And Workshops"

    EVENT = 0 
    WORKSHOP = 1

    CHOICES = (
        (EVENT, 'Event'), 
        (WORKSHOP, 'Workshop'), 
    )

    start_datetime = models.DateTimeField(_('Start date and time'), blank=False, null=False)
    end_datetime = models.DateTimeField(_('End date and time'), blank=False, null=False)
    event_type = models.IntegerField(_('Event type'), choices=CHOICES, default=EVENT)
    title = models.CharField(_('Event Title'), max_length=150, null=False, blank=False, help_text=_("Give Your Event a name."))
    description = models.TextField(_('Event Description'), max_length=2000, null=False, blank=False, help_text=_("Describe your Event here."))
    url = models.CharField(_('URL for Event'), max_length=200, blank=True, null=True)
    participiants = models.ManyToManyField('auth.User', related_name="participiants")
    published = models.BooleanField('published', default=False)

    def get_absolute_url(self): 
        return reverse("events_workshops:show_event", args = (self.id,))

class EventFollower(models.Model): 
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    event_workshop = models.ForeignKey(
        'EventWorkshop', related_name='followers', on_delete=models.CASCADE)
    should_notify = models.BooleanField(default=False, null=False)

