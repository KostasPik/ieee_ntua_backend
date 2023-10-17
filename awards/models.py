from django.db import models
import datetime
from django.core.exceptions import ValidationError
from society.models import Society
# Create your models here.



def year_validation(value):
    current_year = datetime.date.today().year
    minimum_year = datetime.date.today().year - 20
    if value > current_year or value  < minimum_year:
        raise ValidationError('year field must be between {} and {}'.format(current_year, minimum_year))

class Award(models.Model):
    title = models.CharField(max_length=300)
    year = models.IntegerField(validators=[year_validation], help_text="Το έτος που πάρθηκε το βραβείο.")
    society = models.ForeignKey(Society, null=True, blank=True, help_text="Εαν το βραβειο το πήρε το SB αφήστε το κενό.", on_delete=models.CASCADE)


    def __str__(self):
        return self.title