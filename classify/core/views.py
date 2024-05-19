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
            input_dir = os.path.join(md_files_dir,"input_files", file_dir)
            output_dir = os.path.join(md_files_dir,"input_files", "ectracted") 
            print('output_dir::', output_dir)
    
            
            zcf = ZipClassifier() 
            # + "\\" + file_dir[:-4]
            unzipped = unzip_file(input_dir, output_dir)
            
            print('unzipped:::', unzipped)
            
            classified_dir = os.path.join(md_files_dir, "output_files")
            if not os.path.exists(classified_dir):
                os.makedirs(classified_dir)

            ot = zcf.classify(unzipped, classified_dir + "\\" +file_title[:-4])
            print(ot)
            
            context = {"form": FileForm(), "file_dir": "Click the button to download", "output": ot}
            return render(request, "index.html", context)
        else:
            context = {"form": form}
            return render(request, "index.html", context)

    context = {"form": FileForm()}
    return render(request, "index.html", context)




# testing folder showing
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



def files(request):
    if request.user.is_authenticated:
        username = request.user.username
        media_path = settings.MEDIA_ROOT
        user_folder_path = os.path.join(media_path, username, "files", "output_files")

        if os.path.exists(user_folder_path):
            folders = os.listdir(user_folder_path)
            folders_with_path = [os.path.join(user_folder_path, folder) for folder in folders if os.path.isdir(os.path.join(user_folder_path, folder))]
            folder_names = [folder for folder in folders if os.path.isdir(os.path.join(user_folder_path, folder))]

            context = {
                'folder_names': zip(folders_with_path, folder_names)
            }
            return render(request, 'files.html', context)
        else:
            return HttpResponse("Output files folder not found")
    else:
        return redirect('login')
    
    
    
def files_detail(request, folder_name):
    if request.user.is_authenticated:
        username = request.user.username
        media_path = settings.MEDIA_ROOT
        user_folder_path = os.path.join(media_path, username, "files", "output_files", folder_name)

        print("User folder path:", user_folder_path)  # Print user folder path for debugging

        if os.path.exists(user_folder_path) and os.path.isdir(user_folder_path):
            subfolders = [name for name in os.listdir(user_folder_path) if os.path.isdir(os.path.join(user_folder_path, name))]
            context = {
                'folder_name': folder_name,
                'subfolders': subfolders
            }
            return render(request, 'files_detail.html', context)
        else:
            return HttpResponse("Folder not found")
    else:
        return HttpResponse("Unauthorized", status=401)

    
    
    
def folder_images(request, folder_name):
    if request.user.is_authenticated:
        username = request.user.username
        media_path = settings.MEDIA_ROOT
        folder_path = os.path.join(media_path, username, "files", "output_files", "guns", folder_name)

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            images = os.listdir(folder_path)
            image_urls = [os.path.join(settings.MEDIA_URL, username, "files", "output_files", "guns", folder_name, image) for image in images if os.path.isfile(os.path.join(folder_path, image))]
            context = {
                'folder_name': folder_name,
                'image_urls': image_urls
            }
            return render(request, 'folder_images.html', context)
        else:
            return HttpResponse("Folder not found")
    else:
        return HttpResponse("Unauthorized", status=401)

# testing folder showing


def classify(request):

    return





def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})