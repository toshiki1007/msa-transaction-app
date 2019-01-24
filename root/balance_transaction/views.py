from django.http.response import JsonResponse
from .models import *
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import json

def response(status_code, body):
	json_str = json.dumps(body, ensure_ascii=False, indent=4)

	return HttpResponse(json_str, content_type='application/json; charset=UTF-8', status=status_code)

#勘定取引履歴照会
@csrf_exempt
def balance_transaction(request):
	if request.method != 'POST':
		return response(400, None)

	params = json.loads(request.body.decode())

	user_id = params['userId']

	wallet = Wallet.objects.get(user_id = user_id)

	transaction_objects = Transaction.objects.\
		filter(wallet_id = wallet.wallet_id).\
		select_related('wallet_id').\
		select_related('trading_wallet_id').\
		order_by('transaction_date').\
		reverse()

	l = list()

	transactions = {}
	transactions['transactions'] = []

	for obj in transaction_objects:
		transactions['transactions'].append(Transaction.to_dict(obj))

	return response(200, transactions)

#ウォレット照会
@csrf_exempt
def get_wallet(request):
	if request.method != 'POST':
		return response(400, None)

	params = json.loads(request.body.decode())
	user_id = params['userId']
	wallet = Wallet.objects.get(user_id = user_id)

	wallet_data = {
		"walletId": wallet.wallet_id,
		"balance": wallet.balance
	}

	return response(200, wallet_data)