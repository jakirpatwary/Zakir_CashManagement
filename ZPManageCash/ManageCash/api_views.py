from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import AddCash, Expense
from .serializers import AddCashSerializer, ExpenseSerializer


class AddCashViewSet(viewsets.ModelViewSet):
    serializer_class = AddCashSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AddCash.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)