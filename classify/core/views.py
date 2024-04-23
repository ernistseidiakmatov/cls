from django.shortcuts import render, HttpResponse
from django.template import loader
from .forms import FileForm
from django.contrib.auth.models import User
from .models import UserFile
from .utils.unzip import unzip_file
from django.conf import settings
import os

# Create your views here.


def index(request):
    
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()

            file_dir = form.file_dir()
            username = request.user.username

            media_path = settings.MEDIA_ROOT
            input_dir = os.path.join(media_path, username, "files\\input_files", file_dir)
            
            output_dir = os.path.join(media_path, username, "files\\input_files", "extracted")
            unzip_file(input_dir, output_dir)

            context = {"form": FileForm(), "file_dir": file_dir}
            return render(request, "index.html", context)
        else:
            context = {"form": form}
            return render(request, "index.html", context)

    img = UserFile.objects.all()

    context = {"form": FileForm(), "img": img}
    return render(request, "index.html", context)
    
    # template = loader.get_template('index.html')
    
    # return HttpResponse(template.render(request))
    # return HttpResponse("You're looking at question.")


def classify(request):

    return