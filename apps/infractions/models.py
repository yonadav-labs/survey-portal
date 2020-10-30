from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from moss_internal_portal.mixins import UUIDPrimaryKeyMixin
from apps.representatives.models import Representative


class InfractionType(UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=150)
    points = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    wfh_days_forfeit = models.IntegerField("WFH Days Forfeit", default=0, validators=[MinValueValidator(0), MaxValueValidator(365)])
    rolling_months = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(36)])
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Infraction(UUIDPrimaryKeyMixin):
    representative = models.ForeignKey(Representative, on_delete=models.CASCADE, related_name="infractions")
    date = models.DateField()
    type = models.ForeignKey(InfractionType, on_delete=models.CASCADE, related_name="infractions")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.representative} - {self.type}'
