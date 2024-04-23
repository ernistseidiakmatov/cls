from django.db import models
from django.contrib.auth.models import User


# Create your models here.

def user_dir(instance, filename):
    # Get the username of the user uploading the file
    username = instance.user.username
    # Return the path where the file should be saved
    return f"{username}/files/input_files/{filename}"

class UserFile(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_dir)

    