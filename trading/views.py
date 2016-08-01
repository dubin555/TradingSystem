# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .util.operation_with_json_body import get_valid_order_input_from, cancel_order_base_on
import json


def index(request):
    """index view with a "Hello" welcome page
    """
    return HttpResponse("Hello")


@csrf_exempt
def trade(request):
    """View function for trade.do page.
    Only POST method is supported!
    @:return an unique order_id, and result for this post.
    """
    if request.method == "POST":
        received_json_body = json.loads(request.body.decode('utf-8'))
        print(received_json_body)
        valid, order_id, order_item = get_valid_order_input_from(received_json_body)
        return JsonResponse(
                {
                    "result": valid,
                    "order_id": order_id,
                }
        )
    else:
        return HttpResponse("Unknown!")


@csrf_exempt
def cancel_order(request):
    """View function for cancel_order.do page.
    Only POST method is supported!
    when symbol doesn't match order_id, or order_id doesn't exist,or order already done, return False.
    Otherwise return True.
    @:return the order_id, and result for this post.
    """
    if request.method == "POST":
        received_json_body = json.loads(request.body.decode('utf-8'))
        print(received_json_body)
        result, order_id = cancel_order_base_on(received_json_body)
        return JsonResponse(
                {
                    "result": result,
                    "order_id": order_id,

                }
        )
    else:
        return HttpResponse("Unknown!")



