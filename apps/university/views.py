from django.shortcuts import render

# Create your views here.
def upload_base64_image_view(request):
    return render(request, "create_docs.html", {})