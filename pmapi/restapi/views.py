from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin
import rest_framework
from rest_framework.viewsets import ModelViewSet,ViewSet
from .models import Portfolio, Stock, Position
from rest_framework.response import Response
from .serializers import PortfolioSerializer, StockSerializer, PositionSerializer, PositionFileSerializer
import pandas as pd
from django.forms import Form

# Create your views here.
class StockViewSet(ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all().order_by('tick')

class PositionViewSet(ModelViewSet):
    serializer_class = PositionSerializer
    queryset = Position.objects.all()

class PortfolioViewSet(ModelViewSet):
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()

class UploadPositionViewSet(ViewSet):
    serializer_class = PositionFileSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        positionFile = request.FILES.get('positionFile')
        form = Form(request.POST)
        portfolioName = form.data['portfolio']

        positions = pd.read_excel(positionFile)
        for i in positions.index:
            stock, created = Stock.objects.update_or_create(
                tick = positions["SecCode"][i],
                defaults = {'name': positions['Security Desc'][i],
                    'lastprice': positions['Last Px'][i]},
            )

            portfolio, created = Portfolio.objects.update_or_create(
                name = portfolioName
            )

            position, created = Position.objects.update_or_create(
                portfolio = portfolio,
                stock = stock,
                defaults = {'openprice': positions['Open Px'][i],
                    'quantity': positions['Qty (Current)'][i]
                }
            )

        content_type = positionFile.content_type
        response = f'{content_type} is uploaded'
        return Response(response)