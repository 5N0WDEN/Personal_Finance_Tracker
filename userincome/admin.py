from django.contrib import admin
from .models import UserIncome, Source

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'owner', 'source', 'date')
    
admin.site.register(UserIncome, ExpenseAdmin)
admin.site.register(Source)