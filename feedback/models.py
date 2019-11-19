from django.db import models

# Create your models here.
class Feedback(models.Model): 
    class Meta: 
        verbose_name = "User Feedback"
        verbose_name_plural = "User Feedbacks"

    sender = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE)
    headline = models.CharField(verbose_name="Headline", max_length=100, blank=True)
    text = models.TextField(verbose_name="Text", max_length=5000, blank=True)
    
    def __str__(self):
        return '{} {}'.format(self.sender.first_name, self.sender.last_name) if self.sender else "Anonymous"
    
