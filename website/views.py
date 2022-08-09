from django.shortcuts import render, redirect
from django.http import JsonResponse
from . import constants as C
from . import utilities as ut
import json

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
            context["names"] = ut.get_unique_inventory()
            context['data'] = ut.get_all_transactions()
            return render(request, 'dashboard.html', context)
        return render(request, 'index.html', context)
    return JsonResponse(C.unsupported_request_type(request.method))


def dashboard(request):
    if request.method == 'GET':
        # context = ut.create_user_helper(request)
        names = ut.get_unique_inventory()
        unique_part_names = ut.get_unique_part_numbers()
        groups = ut.get_part_numbers_wise_data()
        # print(groups)
        default_part_number = unique_part_names[0]['part_number']
        # print("groups:", json.dumps(groups))
        default_options = groups[default_part_number]
        context = {"names": names, 'part_numbers': unique_part_names,
                   'groups': groups, 'default_part_number': default_part_number
                   ,'default_options': default_options}
        context['data'] = ut.get_all_transactions()
        return render(request, 'dashboard.html', context)
    return JsonResponse(C.unsupported_request_type(request.method))


def inventory(request):
    if request.method == 'GET':
        data = ut.get_inventory()
        names = ut.get_unique_inventory()
        print(list(data.values()))
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
        context = ut.add_transaction(request)
        context['data'] = ut.get_all_transactions()
        context["names"] = ut.get_unique_inventory()
        return render(request, 'dashboard.html', context)
    if request.method == 'GET':
        return redirect("/dashboard/")
    return JsonResponse(C.unsupported_request_type(request.method))


def return_inventory(request):
    if request.method == 'POST':
        context = ut.return_inventory(request)
        context['data'] = ut.get_all_transactions()
        context["names"] = ut.get_unique_inventory()
        return render(request, 'dashboard.html', context)
    if request.method == 'GET':
        return redirect("/dashboard/")
    return JsonResponse(C.unsupported_request_type(request.method))


def show_all_users(request):
    return JsonResponse(ut.show_all_users_helper())

