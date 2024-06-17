from django.shortcuts import render

# Create your views here.
def register_by_invate(request):
    return render(request, "register_by_invate.html", {})