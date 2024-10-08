from .models import *
from django.utils import timezone
from jugaad_data.nse import NSELive
import pytz
import time

nse = NSELive()

IST = pytz.timezone('Asia/Kolkata')

def check_and_execute_orders():
    """
    This function checks pending stock orders and executes them if conditions are met.
    It runs only between 9:00 AM and 4:00 PM IST.
    """
    current_time_ist = timezone.now().astimezone(IST).time()  # Convert current time to IST
    market_open = timezone.datetime.strptime('09:00', '%H:%M').time()
    market_close = timezone.datetime.strptime('16:00', '%H:%M').time()
    # print("tasks")

    if market_open <= current_time_ist <= market_close:
        pending_orders = StockOrder.objects.filter(executed=False)
        for order in pending_orders:
            current_price = get_current_stock_price(order.stock.symbol)

            if order.order_type == 'buy' and current_price <= order.price_at_execution:
                execute_buy_order(order)
            elif order.order_type == 'sell' and current_price >= order.price_at_execution:
                execute_sell_order(order)
    
    time.sleep(10)
    check_and_execute_orders()

def execute_buy_order(order):
    # Logic to process the buy order
    order.executed = True
    order.execution_time = timezone.now()
    user = order.user
    order.save()
    portfolio, created = Portfolio.objects.get_or_create(user = user, defaults={'user': user})
    stock = order.stock
    orderQuantity = order.quantity
    orderPrice = order.price_at_execution
    portfolioStock, created = PortfolioStock.objects.get_or_create(portfolio = portfolio, stock = stock, defaults = {'portfolio': portfolio, 'stock': stock, 'quantity': orderQuantity, 'average_price': orderPrice})
    if not created:
        portQuantity, portPrice = portfolioStock.quantity, portfolioStock.average_price
        portfolioStock.average_price = ((portPrice*portQuantity)+(orderQuantity*orderPrice))/(portQuantity + orderQuantity)
        portfolioStock.quantity = portQuantity + orderQuantity
    # print(portfolioStock.average_price, portfolioStock.quantity)
    portfolioStock.save()

def execute_sell_order(order):
    # Logic to process the sell order
    order.executed = True
    order.execution_time = timezone.now()
    order.save()
    user = order.user
    portfolio = Portfolio.objects.get(user = user)
    stock = order.stock
    orderQuantity = order.quantity
    orderPrice = float(order.price_at_execution)
    portfolioStock = PortfolioStock.objects.get(portfolio = portfolio, stock = stock)
    portQuantity, portPrice = portfolioStock.quantity, float(portfolioStock.average_price)
    if portQuantity!=orderQuantity:
        portfolioStock.average_price = ((portPrice*portQuantity)-(orderQuantity*orderPrice))/(portQuantity - orderQuantity)
        portfolioStock.quantity = portQuantity - orderQuantity
        portfolioStock.save()
    else:
        portfolioStock.delete()
    fund = Funds.objects.get(user = user)
    fund.balance = float(fund.balance) + orderQuantity*orderPrice
    fund.save()

def get_current_stock_price(symbol):
    q = nse.stock_quote(symbol)
    return q['priceInfo']['lastPrice']