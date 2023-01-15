from django.db import models
import datetime
import time
# Create your models here.


class Users(models.Model):
    username = models.CharField('User Name', null=False, max_length = 50)
    password = models.CharField('User Password', max_length=50)

    def __str__(self):
        return self.username

def get_filepath(filename):
    old_filename = filename
    ts = time.time()
    timeNow = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S')
    filename = "%s%s" % (timeNow, old_filename)
    return filename
class Photo(models.Model):
    name = models.CharField(max_length=100, default="Image")
    id = models.AutoField(primary_key=True)
    uploader = models.ForeignKey(Users, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Photo_History(models.Model):
    image = models.ImageField(upload_to="media/results")
    upload_time = models.DateTimeField(auto_now_add=True, blank=True)
    photo_id = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.CASCADE)


class Photo_Details(models.Model):
    id = models.AutoField(primary_key=True)
    photo = models.ForeignKey(Photo_History, null=True, blank=True, on_delete=models.CASCADE)
    object_name = models.CharField(max_length=50, null=True)
    object_count = models.IntegerField(null=True)
    