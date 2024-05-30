from django.contrib import admin
from .models import Expence, Category
# Register your models here.


'''class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'owner', 'category', 'date')
    search_fields = ('amount', 'description', 'owner', 'category', 'date')'''

#admin.site.register(Expence, ExpenseAdmin)
admin.site.register(Expence)
admin.site.register(Category)
