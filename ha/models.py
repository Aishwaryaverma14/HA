from django.db import models
class HAConfig(models.Model):
    virtual_ip = models.GenericIPAddressField()

    master_ip = models.GenericIPAddressField()
    slave_ip = models.GenericIPAddressField()

    interface = models.CharField(max_length=20)

    master_priority = models.IntegerField(default=100)
    slave_priority = models.IntegerField(default=90)

    def __str__(self):
        return self.virtual_ip

# Create your models here.
