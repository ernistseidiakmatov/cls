from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from .forms import FileForm
from django.contrib.auth.models import User
from .models import UserFile
from .utils.unzip import unzip_file
from .utils.zipCF import ZipClassifier
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
            print("meida path: ", media_path)

            md_files_dir = os.path.join(media_path, username, "files")
            input_dir = os.path.join(md_files_dir,"input_files", file_dir)
            output_dir = os.path.join(md_files_dir,"input_files", "ectracted") 
    
            
            zcf = ZipClassifier() 
            unzipped = unzip_file(input_dir, output_dir)+ "\\" + file_dir[:-4]
            
            classified_dir = os.path.join(md_files_dir, "output_files")
            if not os.path.exists(classified_dir):
                os.makedirs(classified_dir)

            ot = zcf.classify(unzipped, classified_dir + "\\" +file_dir[:-4])
            print(ot)
            
            context = {"form": FileForm(), "file_dir": "Click the button to download", "output": ot}
            return render(request, "index.html", context)
        else:
            context = {"form": form}
            return render(request, "index.html", context)

    context = {"form": FileForm()}
    return render(request, "index.html", context)


def classify(request):
    pass