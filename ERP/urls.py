from django.urls import path
from .views import StockAPIView, SalesAPIView, ReportsApiView

urlpatterns = [
    path('stock/', StockAPIView.as_view()),
    path('sales/', SalesAPIView.as_view()),
    path('reports/', ReportsApiView.as_view()),

]
