from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore

class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.symbol

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cash_balance = models.DecimalField(max_digits=15, decimal_places=2, default=100000.00)  # Starting cash balance
    stocks = models.ManyToManyField('Stock', through='StockOwnership', related_name='portfolios')

    def __str__(self):
        return f"{self.user.username}'s Portfolio"

class StockOwnership(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='stock_ownerships')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    average_price = models.DecimalField(max_digits=10, decimal_places=2)  # Average purchase price per share

    class Meta:
        unique_together = ('portfolio', 'stock')

    def __str__(self):
        return f"{self.quantity} shares of {self.stock.symbol} in {self.portfolio.user.username}'s Portfolio"
