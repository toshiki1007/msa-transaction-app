from django.http.response import JsonResponse
from .models import *
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import json

def response(status_code, body, message):
	return {
		'statusCode': status_code,
		'body': body,
		'errorMessage': message
	}

#勘定取引履歴照会
@csrf_exempt
def balance_transaction(request):
	if request.method != 'POST':
		return response(400, None, 'invalid access error')

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

	return JsonResponse(response(200, transactions, None))