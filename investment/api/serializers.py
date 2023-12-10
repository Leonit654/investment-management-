from rest_framework import serializers
from investment.models import Cash_flows, Trades


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trades
        fields = "__all__"


class CashFlowSerializer(serializers.ModelSerializer):
    trade = TradeSerializer()

    class Meta:
        model = Cash_flows
        fields = "__all__"
