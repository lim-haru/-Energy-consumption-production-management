from django.db import models
from .utils import sendTransaction
import hashlib
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

class Energy(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    produced_energy_in_watt = models.FloatField(verbose_name='Enegia Prodotta')
    consumed_energy_in_watt = models.FloatField(verbose_name='Enegia Consumata')
    hash = models.CharField(max_length=32, blank=True, default=None, null=True)
    txId = models.CharField(max_length=66, blank=True, default=None, null=True, verbose_name='Id Transazione')

    def __str__(self):
        return self.datetime.strftime('%Y/%m/%d - %H:%M') #return self.date.strftime('%Y/%m/%d %H:%M') + ' - ' + self.time.strftime('%H:%M')

    def writeOnChain(self, sender=None, instance=None, **kwargs):
        if not self.hash or not self.txId:
            data = f"Produced energy in watt= {self.produced_energy_in_watt} \nConsumed energy in watt= {self.consumed_energy_in_watt}"
            self.hash = hashlib.sha256(data.encode('utf-8')).hexdigest()
            self.txId = sendTransaction(self.hash)
            self.save()

@receiver(post_save, sender=Energy)
def call_writeOnChain(sender, instance, **kwargs):
    instance.writeOnChain()