from django.db import models
from django.contrib.auth.models import User
import random, string


def randomid():
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for each in range(16))
        
class Wallet(models.Model):
    walletid = models.CharField(max_length=16, default=randomid)
    owned = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False,
                related_name="owner")
    status = models.CharField(max_length=50,default="disabled")
    balance = models.ManyToManyField('Balance', related_name='balance_amount')
    enabled_at = models.DateTimeField(auto_now=True)

    def owned_by(self):
        return User.objects.get(id = self.owned_id).username    

    def balance_amount(self):
        dep = 0
        wid = 0
        for balance in self.balance.all():
            if balance.type == "Deposit":
               dep += balance.amount
            if balance.type == "Withdrawal":
               wid += balance.amount
        bal = dep - wid
        return bal

    def amount(self):
        bal = 0
        for balance in self.balance.all()[1:]:
            bal = balance.amount
        return bal

    def deposited_by(self):
        # depst = ""
        for balance in self.balance.all()[1:]:
            depst = User.objects.get(id = balance.deposited_by_id)    
        return depst.username

    def deposited_at(self):
        # depst = ""
        for balance in self.balance.all()[1:]:
            depst = balance.deposited_at    
        return depst

    def withdrawn_by(self):
        # depst = ""
        for balance in self.balance.all()[1:]:
            depst = User.objects.get(id = balance.deposited_by_id)    
        return depst.username

    def withdrawn_at(self):
        # depst = ""
        for balance in self.balance.all()[1:]:
            depst = balance.deposited_at    
        return depst

        

    def reference_id(self):
        ref = ""    
        for balance in self.balance.all()[1:]:
            ref = balance.reference_id    
        return ref
                

FILE_CHOICES = (
    ("Deposit", "Deposit"),
    ("Withdrawal", "Withdrawal"),
)
class Balance(models.Model):
    type = models.CharField(max_length=10, choices=FILE_CHOICES, null=False, blank=False)
    amount = models.FloatField(blank=True, null=True)
    deposited_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                related_name="depositor")
    reference_id = models.CharField(max_length=32, null=True, blank=True)
    deposited_at = models.DateTimeField(auto_now=True)
    

    