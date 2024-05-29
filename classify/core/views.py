from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from .forms import FileForm
from django.contrib.auth.models import User
from .models import UserFile
from .utils.unzip import unzip_file
from .utils.zipCF import ZipClassifier
from django.conf import settings
import os
from django.core.files.storage import default_storage
from django.http import FileResponse, Http404
import zipfile

def index(request):
    
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()

            file_dir = form.file_dir()
            file_title = form.file_title()
            username = request.user.username

            media_path = settings.MEDIA_ROOT
            print("meida path: ", media_path)

            md_files_dir = os.path.join(media_path, username, "files")
            input_dir = os.path.join(md_files_dir,"input_files", "temp", file_dir)
            output_dir = os.path.join(md_files_dir,"input_files", "ectracted") 
            print('output_dir::', output_dir)
    
            
            zcf = ZipClassifier() 
            # + "\\" + file_dir[:-4]
            unzipped = unzip_file(input_dir, output_dir)
            
            print('unzipped:::', unzipped)
            
            classified_dir = os.path.join(md_files_dir, "output_files")
            if not os.path.exists(classified_dir):
                os.makedirs(classified_dir)

            ot = zcf.classify(unzipped, classified_dir + "\\" +file_title)
            print(ot)
            
            context = {"form": FileForm(), "file_dir": "Click the button to download", "output": ot}
            return render(request, "index.html", context)
        else:
            context = {"form": form}
            return render(request, "index.html", context)

    context = {"form": FileForm()}
    return render(request, "index.html", context)



def home(request):
    if request.user.is_authenticated:
        username = request.user.username
        media_path = settings.MEDIA_ROOT
        output_files_path = os.path.join(media_path, username, "files", "output_files")

        folder_names = []

        if os.path.exists(output_files_path) and os.path.isdir(output_files_path):
            folder_names = [name for name in os.listdir(output_files_path) if os.path.isdir(os.path.join(output_files_path, name))]

        print("Folder names:", folder_names)

        context = {
            'folder_names': folder_names
        }
        return render(request, 'home.html', context)
    else:
        return redirect('login')

    

def files_detail(request, folder_path):
    if request.user.is_authenticated:
        username = request.user.username
        media_path = settings.MEDIA_ROOT
        full_folder_path = os.path.join(media_path, username, "files", "output_files", folder_path)

        subfolder_names = []
        image_files = []

        if os.path.exists(full_folder_path) and os.path.isdir(full_folder_path):
            for item in os.listdir(full_folder_path):
                item_path = os.path.join(full_folder_path, item)
                if os.path.isdir(item_path):
                    subfolder_names.append(item)
                elif item.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    relative_path = os.path.relpath(item_path, media_path)
                    image_files.append({
                        'url': default_storage.url(relative_path),
                        'name': item
                    })

        context = {
            'folder_path': folder_path,
            'subfolder_names': subfolder_names,
            'image_files': image_files
        }
        return render(request, 'files_detail.html', context)
    else:
        return redirect('login')



def downloads(request):
    if not request.user.is_authenticated:
        return redirect('login')

    username = request.user.username
    media_path = settings.MEDIA_ROOT
    output_files_path = os.path.join(media_path, username, "files", "output_files")

    if request.method == "POST":
        down_folder = request.POST.get("input")
        if down_folder:
            folder_path = os.path.join(output_files_path, down_folder)
            zip_file_path = os.path.join(output_files_path, down_folder + ".zip")

            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, start=folder_path)
                            zipf.write(file_path, arcname)

                response = FileResponse(open(zip_file_path, 'rb'), as_attachment=True, filename=down_folder + ".zip")
                return response
            else:
                raise Http404("Folder does not exist")

    folder_names = []
    if os.path.exists(output_files_path) and os.path.isdir(output_files_path):
        folder_names = [name for name in os.listdir(output_files_path) if os.path.isdir(os.path.join(output_files_path, name))]

    context = {
        'folder_names': folder_names
    }

    return render(request, "download.html", context)




def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})