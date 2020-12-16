from rest_framework import serializers
from rest_framework.fields import CharField
from .models import Portfolio, Position, Stock
from rest_framework.serializers import Serializer, FileField

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'
        
class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'

class PositionFileSerializer(Serializer):
    positionFile = FileField()
    portfolio = CharField(max_length=20)
    class Meta:
        fields = '__all__'