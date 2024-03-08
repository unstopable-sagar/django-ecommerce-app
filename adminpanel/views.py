from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.auth import admin_only

# Create your views here.
@login_required
@admin_only
def show_dashboard(request):
    return render(request,'adminspage/dashboard.html')
