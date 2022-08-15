from django.shortcuts import render, redirect
from django.http import JsonResponse
from . import constants as C
from . import utilities as ut
import json
from django.views.decorators.csrf import csrf_exempt
from . import default_reponses as res


# Create your views here.
def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})
    return JsonResponse(C.unsupported_request_type(request.method))


def create_user(request):
    if request.method == 'POST':
        context = ut.create_user_helper(request)
        # print(context)
        return render(request, 'index.html', context)
    return JsonResponse(C.unsupported_request_type(request.method))


def login(request):
    if request.method == 'POST':
        context = ut.login_helper(request)
        # print(context)
        if context['success']:
            context = ut.get_dashboard_context()
            return render(request, 'dashboard.html', context)
        return render(request, 'index.html', context)
    return JsonResponse(C.unsupported_request_type(request.method))


def dashboard(request):
    if request.method == 'GET':
        # context = ut.create_user_helper(request)
        context = ut.get_dashboard_context()
        return render(request, 'dashboard.html', context)
    return JsonResponse(C.unsupported_request_type(request.method))


def inventory(request):
    if request.method == 'GET':
        data = ut.get_inventory()
        names = ut.get_unique_inventory()
        # print(list(data.values()))
        # ut.delete_transactions()
        context = {"data": data, "names": names}
        # context['data'] = ut.get_all_transactions()
        return render(request, 'inventory.html', context)
    return JsonResponse(C.unsupported_request_type(request.method))


def add_inventory(request):
    if request.method == 'POST':
        context = ut.add_inventory(request)
        context['data'] = ut.get_inventory()
        context["names"] = ut.get_unique_inventory()
        return render(request, 'inventory.html', context)
    if request.method == 'GET':
        return redirect("/inventory/")
    return JsonResponse(C.unsupported_request_type(request.method))


def remove_inventory(request):
    if request.method == 'POST':
        context = ut.remove_inventory(request)
        context['data'] = ut.get_inventory()
        context["names"] = ut.get_unique_inventory()
        return render(request, 'inventory.html', context)
    if request.method == 'GET':
        return redirect("/inventory/")
    return JsonResponse(C.unsupported_request_type(request.method))


def add_transaction(request):
    if request.method == 'POST':
        context = ut.get_dashboard_context()
        return render(request, 'dashboard.html', context)
    if request.method == 'GET':
        context = ut.get_dashboard_context()
        return redirect("/dashboard/")
    return JsonResponse(C.unsupported_request_type(request.method))


def return_inventory(request):
    if request.method == 'POST':
        context = ut.get_dashboard_context()
        return render(request, 'dashboard.html', context)
    if request.method == 'GET':
        return redirect("/dashboard/")
    return JsonResponse(C.unsupported_request_type(request.method))


def show_all_users(request):
    return JsonResponse(ut.show_all_users_helper())


@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        return JsonResponse(ut.login_api_helper(request))
    return JsonResponse(res.wrong_api_call_response(request.method))



@csrf_exempt
def dashboard_api(request):
    if request.method == 'GET':
        return JsonResponse(ut.dashboard_api_helper())
    return JsonResponse(res.wrong_api_call_response(request.method))


@csrf_exempt
def add_inventory_api(request):
    if request.method == 'POST':
        return JsonResponse(ut.add_inventory_api_helper(request))
    return JsonResponse(res.wrong_api_call_response(request.method))


@csrf_exempt
def add_employee_api(request):
    if request.method == 'POST':
        return JsonResponse(ut.add_employee_api_helper(request))
    return JsonResponse(res.wrong_api_call_response(request.method))

@csrf_exempt
def available_quantity_api(request):
    if request.method == 'POST':
        return JsonResponse(ut.available_quantity_api_helper(request))
    return JsonResponse(res.wrong_api_call_response(request.method))


@csrf_exempt
def add_transaction_api(request):
    if request.method == 'POST':
        return JsonResponse(ut.add_transaction_api_helper(request))
    return JsonResponse(res.wrong_api_call_response(request.method))


@csrf_exempt
def inventory_api(request):
    if request.method == 'GET':
        return JsonResponse(ut.inventory_api_helper(request))
    return JsonResponse(res.wrong_api_call_response(request.method))


@csrf_exempt
def return_inventory_api(request):
    if request.method == 'POST':
        return JsonResponse(ut.return_inventory_api_helper(request))
    return JsonResponse(res.wrong_api_call_response(request.method))