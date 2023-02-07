from time import timezone
from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils import timezone
import calendar
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
class Month(models.Model):
    month_name = models.CharField(max_length=35, default='')
    year = models.PositiveIntegerField(default=None)
    
    def __str__(self):
        return self.month_name
    
class Day(models.Model):
    day_name = models.CharField(max_length=35, default='')
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='days', default=None)
    
    def __str__(self):
        return self.day_name
    
@receiver(post_save, sender=Month)
def create_days(sender, instance, created, **kwargs):
    if created:
        month_int = datetime.strptime(instance.month_name, '%B').month
        # Get the number of days in the month
        num_days = calendar.monthrange(instance.year, month_int)[1]
        
        # Create a Day object for each day in the month
        for i in range(1, num_days+1):
            day = Day(day_name=str(i), month=instance)
            day.save()
class Note(models.Model):  
    day = models.ForeignKey(Day, default=None, on_delete=models.CASCADE, related_name='attached_notes')
    note_name = models.CharField(max_length=35, default='')
    note_text = models.TextField(blank=True, default='')
    pub_date = models.DateTimeField('date published', default=timezone.now())

    def __str__(self):
        return self.note_name
    