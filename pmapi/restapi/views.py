from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin
import rest_framework
from rest_framework import response
from rest_framework.viewsets import ModelViewSet,ViewSet
from .models import Portfolio, Stock, Position
from rest_framework.response import Response
from .serializers import PortfolioSerializer, StockSerializer, PositionSerializer, PositionFileSerializer
import pandas as pd
import math
from django.forms import Form
from rest_framework.decorators import action

# Create your views here.
class StockViewSet(ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all().order_by('tick')

class PositionViewSet(ModelViewSet):
    serializer_class = PositionSerializer
    queryset = Position.objects.all()

    def list(self, request):
        portfolio = request.GET['portfolio']
        return Response(PositionSerializer(Position.objects.filter(portfolio=portfolio), many=True).data)

    def create(self, request):
        port = Portfolio.objects.filter(name = request.data['portfolio'])[0]
        stock = Stock.objects.filter(tick = request.data['stock'])[0]

        position, created = Position.objects.update_or_create(
                portfolio = port,
                stock = stock,
                defaults = {
                    'openprice' : request.data['openprice'],
                    'quantity' : request.data['quantity'],
                },
        )
        if created:
            return Response(f"Position for {request.data['portfolio']} {request.data['stock']} is crated.")
        else:
            return Response(f"Position for {request.data['portfolio']} {request.data['stock']} is updated.")

class PortfolioViewSet(ModelViewSet):
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()

    def create(self, request):
        portfolio, created = Portfolio.objects.update_or_create(
            name = request.data['name'],
        )

        if created:
            return Response(f"Portfolio {request.data['name']} is created.")
        else:
            return Response(f"Portfolio {request.data['name']} is updated.")

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
            #Skip empty quantity
            if math.isnan(positions['Qty (Current)'][i]):
                continue

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