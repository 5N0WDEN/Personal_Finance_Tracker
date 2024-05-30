from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserIncome, Source
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from userpreferences.models import UserPreferences

# Create your views here.
@csrf_exempt
def search_incomes(request):
    data = []
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText', '')
        incomes = UserIncome.objects.filter(
            amount__icontains = search_str, owner=request.user) or UserIncome.objects.filter(
            date__icontains = search_str, owner=request.user) or UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) or UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)

        data = incomes.values()

    return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        user_preferences = UserPreferences.objects.get(user=request.user)
        currency = user_preferences.currency
    except UserPreferences.DoesNotExist:
        currency = 'INR - Indian Rupee'
    context = {
        'income' : income,
        'page_obj' : page_obj,
        'currency' : currency,
    }
    return render(request, 'income/index.html', context)

@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources' : sources,
        'values' : request.POST,
    }
    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        source = request.POST['source']
        date = request.POST['income_date']
        description = request.POST['description']
        if not amount or not description or not date or not source:
            if not amount:
                messages.error(request, "Amount is required.")
            if not description:
                messages.error(request, "Description is required.")
            if not date:
                messages.error(request, "Date is required.")
            if not source:
                messages.error(request, "Source is required.")
            return render(request, 'income/add_income.html', context)
        else:
            UserIncome.objects.create(owner=request.user, amount=amount, date=date, source=source, description=description)
            messages.success(request, "Income saved successfully.")
            return redirect('income')
            
@login_required(login_url='/authentication/login')
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    income.date = income.date.strftime('%Y-%m-%d')
    context = {
        'income' : income,
        'values' : income,
        'sources' : sources,
    }
    if request.method == "GET":
        return render(request, 'income/edit-income.html', context)
    else:
        if request.method == 'POST':
            amount = request.POST['amount']
            source = request.POST['source']
            date = request.POST['income_date']
            description = request.POST['description']
            if not amount or not description or not date or not source:
                if not amount:
                    messages.error(request, "Amount is required.")
                if not description:
                    messages.error(request, "Description is required.")
                if not date:
                    messages.error(request, "Date is required.")
                if not source:
                    messages.error(request, "Source is required.")
                return render(request, 'income/edit-income.html', context)
            else:
                income.owner = request.user
                income.amount = amount 
                income.date = date 
                income.source = source
                income.description = description
                income.save()
                messages.success(request, "Income updated successfully.")
                return redirect('income')

@login_required(login_url='/authentication/login')
def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, "Income removed.")
    return redirect('income')