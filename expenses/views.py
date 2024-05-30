from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expence, Category
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from userpreferences.models import UserPreferences

# Create your views here.
@csrf_exempt
def search_expenses(request):
    data = []
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText', '')
        expenses = Expence.objects.filter(
            amount__icontains = search_str, owner=request.user) or Expence.objects.filter(
            date__icontains = search_str, owner=request.user) or Expence.objects.filter(
            description__icontains=search_str, owner=request.user) or Expence.objects.filter(
            category__icontains=search_str, owner=request.user)

        data = expenses.values()

    return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expence.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        user_preferences = UserPreferences.objects.get(user=request.user)
        currency = user_preferences.currency
    except UserPreferences.DoesNotExist:
        currency = 'INR - Indian Rupee'
    context = {
        'expenses' : expenses,
        'page_obj' : page_obj,
        'currency' : currency,
    }
    return render(request, 'expenses/index.html', context)

@login_required(login_url='/authentication/login')
def add_expenses(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories,
        'values' : request.POST,
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expenses.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        category = request.POST['category']
        date = request.POST['expense_date']
        description = request.POST['description']
        if not amount or not description or not date or not category:
            if not amount:
                messages.error(request, "Amount is required.")
            if not description:
                messages.error(request, "Description is required.")
            if not date:
                messages.error(request, "Date is required.")
            if not category:
                messages.error(request, "Category is required.")
            return render(request, 'expenses/add_expenses.html', context)
        else:
            Expence.objects.create(owner=request.user, amount=amount, date=date, category=category, description=description)
            messages.success(request, "Expense saved successfully.")
            return redirect('expenses')
            
@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expence.objects.get(pk=id)
    categories = Category.objects.all()
    expense.date = expense.date.strftime('%Y-%m-%d')
    context = {
        'expense' : expense,
        'values' : expense,
        'categories' : categories,
    }
    if request.method == "GET":
        return render(request, 'expenses/edit-expenses.html', context)
    else:
        if request.method == 'POST':
            amount = request.POST['amount']
            category = request.POST['category']
            date = request.POST['expense_date']
            description = request.POST['description']
            if not amount or not description or not date or not category:
                if not amount:
                    messages.error(request, "Amount is required.")
                if not description:
                    messages.error(request, "Description is required.")
                if not date:
                    messages.error(request, "Date is required.")
                if not category:
                    messages.error(request, "Category is required.")
                return render(request, 'expenses/edit-expenses.html', context)
            else:
                expense.owner = request.user
                expense.amount = amount 
                expense.date = date 
                expense.category = category
                expense.description = description
                expense.save()
                messages.success(request, "Expense updated successfully.")
                return redirect('expenses')

@login_required(login_url='/authentication/login')
def delete_expense(request, id):
    expense = Expence.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense removed.")
    return redirect('expenses')