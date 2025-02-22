# serializers.py

from rest_framework import serializers

from dues.models import BankAccount, DuesEntry, DuesPayPeriod, Transaction


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class AllDuesPayPeriodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DuesPayPeriod
        fields = '__all__'



class AllDuesEntrysSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = DuesEntry
        fields = '__all__'

    def get_full_name(self, obj):
        first_name = obj.user.first_name
        last_name = obj.user.last_name
        if first_name and last_name:
            return first_name + ' ' + last_name
        return None








class DuesEntryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DuesEntry
        fields = '__all__'



class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(max_length=255, required=False)

class WithdrawSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(max_length=255, required=False)

class TransferSerializer(serializers.Serializer):
    to_account_id = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(max_length=255, required=False)


