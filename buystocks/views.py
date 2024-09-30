from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json,html
from urllib.parse import unquote
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime


@login_required(login_url='/login/')
def add_funds(request):
    if request.method == 'POST':
        try:
            # Parse the request body as JSON
            body = json.loads(request.body)
            amount = body.get('amount', 0)
            user = request.user
            
            if amount <= 0:
                return JsonResponse({"error": "Amount must be greater than zero."}, status=400)

            # Create the transaction
            transaction = Transaction.objects.create(
                user=user,
                transaction_type='Deposit',
                amount=amount,
                transaction_date=datetime.now()  # Include the date if necessary
            )
            transaction.save()

            # Update the user's funds
            fundobj = get_object_or_404(Funds, user=user)
            fundobj.balance = float(fundobj.balance) + amount
            fundobj.save()

            return JsonResponse(data={'message': 'Success'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)  # Catch all other exceptions
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def serialize_transactions(transactions):
    serialized = []
    for transaction in transactions:
        serialized.append({
            'id': transaction['id'],
            'user_id': transaction['user_id'],
            'transaction_type': transaction['transaction_type'],
            'amount': float(transaction['amount']),  # Convert Decimal to float
            'transaction_date': transaction['transaction_date'].strftime('%Y-%m-%d %H:%M')  # Convert datetime to ISO format string
        })
    return serialized


@login_required(login_url='/login/')
def fundspage(request):
    user = request.user
    
    # Get or create a Fund instance for the user
    fund, created = Funds.objects.get_or_create(user=user, defaults={'balance': 0.00})

    # Fetch transactions for the user, ordered by transaction date
    transactions = list(Transaction.objects.filter(user=user).order_by('-transaction_date').values())

    # Serialize transactions to make them JSON compatible
    serialized_transactions = serialize_transactions(transactions)

    context = {
        'fund': fund,
        'transactions': json.dumps(serialized_transactions),  # Use serialized transactions here
    }

    return render(request, 'fundspage.html', context=context)

@login_required(login_url='/login/')
def withdraw_funds(request):
    if request.method == 'POST':
        try:
            # Parse the request body as JSON
            body = json.loads(request.body)
            amount = body.get('amount', 0.00)
            user = request.user
            
            # Get the user's funds
            fundobj = get_object_or_404(Funds, user=user)
            
            # Check if there are sufficient funds
            if fundobj.balance >= amount:
                # Create a transaction record
                transaction = Transaction.objects.create(
                    user=user,
                    transaction_type='Withdraw',
                    amount=amount
                )
                transaction.save()
                
                # Deduct the amount from the balance
                fundobj.balance = float(fundobj.balance) - amount
                fundobj.save()
                
                return JsonResponse(data={'message': 'Success'}, status=200)
            else:
                return JsonResponse({"error": "Insufficient funds"}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
