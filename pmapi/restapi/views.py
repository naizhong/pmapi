from django.shortcuts import render
from rest_framework import viewsets
from .models import Portfolio, Stock, Position
from .serializers import PortfolioSerializer, StockSerializer, PositionSerializer

# Create your views here.
class StockViewSet(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all().order_by('tick')

class PositionViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer
    queryset = Position.objects.all()

class PortfolioViewSet(viewsets.ModelViewSet):
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()