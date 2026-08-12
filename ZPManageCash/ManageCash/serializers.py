from rest_framework import serializers

from .models import AddCash, Expense


class AddCashSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddCash
        fields = [
            "id",
            "source",
            "datetime",
            "amount",
            "description",
        ]
        read_only_fields = ["id"]


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = [
            "id",
            "description",
            "amount",
            "datetime",
        ]
        read_only_fields = ["id"]