from rest_framework.routers import DefaultRouter

from .api_views import AddCashViewSet, ExpenseViewSet


router = DefaultRouter()

router.register(
    r"cash",
    AddCashViewSet,
    basename="cash"
)

router.register(
    r"expenses",
    ExpenseViewSet,
    basename="expense"
)

urlpatterns = router.urls