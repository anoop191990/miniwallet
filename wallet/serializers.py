from rest_framework import serializers
from wallet.models import *

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['status']

class ListWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['walletid','owned_by','status','balance_amount','enabled_at']

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['walletid','deposited_by','status','amount','deposited_at','reference_id']

class WidrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['walletid','withdrawn_by','status','amount','withdrawn_at','reference_id']



    