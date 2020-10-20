from django.db import models

from moss_internal_portal.mixins import (CreatedModifiedMixin, UUIDPrimaryKeyMixin)


class Representative(UUIDPrimaryKeyMixin, CreatedModifiedMixin):
    TYPE = (
        ('AGENT', 'Agent'),
        ('IPR', 'IPR')
    )

    STATUS = (
        ('ACTIVE', 'Active'),
        ('TERMINATED', 'Terminated')
    )

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField("Middle Initial", max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField("Work E-mail Address", unique=True)
    type = models.CharField(max_length=50, choices=TYPE, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS)
    last_status_date = models.DateField("Status Date")
    last_hire_date = models.DateField()
    division = models.CharField(max_length=150, blank=True, null=True)
    department = models.CharField(max_length=150, blank=True, null=True)
    workgroup = models.CharField("Work Group", max_length=150)

    @property
    def full_name(self):
        name = f'{self.first_name} {self.last_name}' if not self.middle_name else f'{self.first_name} {self.middle_name} {self.last_name}'
        return name 
