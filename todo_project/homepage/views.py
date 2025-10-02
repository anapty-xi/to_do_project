from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def homepage(requset):
    return render(requset, 'homepage/homepage.html')
