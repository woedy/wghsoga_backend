from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models.signals import pre_save

from wghsoga_project.utils import unique_account_id_generator, unique_dues_id_generator, unique_transaction_id_generator


User = get_user_model()

class BankAccount(models.Model):

    year_group = models.CharField(max_length=20, unique=True)
    account_id = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    is_archived = models.BooleanField(default=False)


    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.year_group} - {self.account_id}"

    def deposit(self, amount, description=None):
        if amount > 0:
            self.balance += amount
            self.save()
            Transaction.objects.create(
                bank_account=self,
                transaction_type='Deposit',
                amount=amount,
                description=description
            )
            return True
        return False

    def withdraw(self, amount, description=None):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.save()
            Transaction.objects.create(
                bank_account=self,
                transaction_type='Withdrawal',
                amount=amount,
                description=description
            )
            return True
        return False

def pre_save_account_id_receiver(sender, instance, *args, **kwargs):
    if not instance.account_id:
        instance.account_id = unique_account_id_generator(instance)

pre_save.connect(pre_save_account_id_receiver, sender=BankAccount)

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Transfer', 'Transfer'),
    ]

    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_id = models.CharField(max_length=20, unique=True)

    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.bank_account.account_id} - {self.transaction_type} - {self.amount}"



def pre_save_transaction_id_receiver(sender, instance, *args, **kwargs):
    if not instance.transaction_id:
        instance.transaction_id = unique_transaction_id_generator(instance)

pre_save.connect(pre_save_transaction_id_receiver, sender=Transaction)



class DuesPayPeriod(models.Model):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    is_archived = models.BooleanField(default=False)


    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.start_date} - {self.end_date}'

class DuesEntry(models.Model):
    dues_id = models.CharField(max_length=200, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pay_period = models.ForeignKey(DuesPayPeriod, on_delete=models.CASCADE)
    amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, null=True, blank=True)
    reference = models.CharField(max_length=100, blank=True, null=True)

    is_archived = models.BooleanField(default=False)


    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} - {self.pay_period}'


def pre_save_dues_id_receiver(sender, instance, *args, **kwargs):
    if not instance.dues_id:
        instance.dues_id = unique_dues_id_generator(instance)

pre_save.connect(pre_save_dues_id_receiver, sender=DuesEntry)

