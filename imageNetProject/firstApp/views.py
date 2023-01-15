from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
# from yolo_detection_images import detect_image
# from keras.models import load_model 
from torch_utils import show_img
from keras.preprocessing import image 
# import tensorflow.compat.v1 as tf
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from .models import *
import cv2
import json
# tf.disable_v2_behavior()
import json 
import datetime

img_height, img_width = 224, 224 
# Create your views here.

@csrf_exempt
def login(request):
    if request.session.has_key('is_logged'):
        return redirect('index')
    if request.POST:
        if 'user_name' not in request.POST:
            return render(request, 'login.html')
        username_entry = request.POST['user_name']
        password = request.POST['password']
        count = Users.objects.filter(username=username_entry).count()
        if count > 0:
            user_password = Users.objects.values('password').filter(username=username_entry)[0]
            if password == user_password['password']:
                request.session['is_logged'] = True
                request.session['user_id'] = request.POST['user_name']
                return redirect('index')
            else:
                messages.error(request, "Invalid Password")
                return render(request, 'login.html')
        else:
            messages.error(request, "Invalid Username")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
# q = "select p.id, p.name, h.image, h.upload_time, u.username from firstApp_Users u firstApp_Photo_History h, firstApp_Photo p;"
        # photos = Photo_History.objects.raw(q)

        # photos = Photo_History.objects.all().filter(photo_id__in=Photo.objects.filter(
        #     uploader=Users.objects.filter(username=current_user_id)[0]
        # )
        # ).values('image', 'upload_time', 'photo_id', 'Photo__name')
def history(request):
    if request.session.has_key('is_logged'):
        current_user_id= request.session['user_id']
        # q = "select * from firstApp_Photo where uploader_id=%s;"
        # photos = Photo.objects.raw(q, [str(Users.objects.filter(username=current_user_id)[0])])
        # photos = Photo.objects.raw(q)
        # q = "select p.id, p.name, h.image, h.upload_time from firstApp_Photo_History h, firstApp_Photo p where p.uploader_id=%s;"
        # photos = Photo.objects.raw(q, [str(Users.objects.filter(username=current_user_id)[0])])
        q = "select h.id, p.name, h.image, h.upload_time, p.uploader_id from firstApp_Photo_History h inner join firstApp_Photo p on h.photo_id_id = p.id where p.uploader_id=%s;"
        photos = Photo.objects.raw(q, [str(Users.objects.filter(username=current_user_id)[0].id)])
            # print(p.upload_time)
        return render(request, 'history.html', {'ID':current_user_id, 'photos':photos})
    else:
        return redirect('login')

def login_submit(request):
    return redirect('index')

def index(request):
    if request.session.has_key('is_logged'):
        current_user_id= request.session['user_id']
        photos = Photo.objects.all().filter(uploader=Users.objects.filter(username=current_user_id)[0])
        return render(request, 'index.html', {'ID':current_user_id, 'photos': photos})
    else:
        return redirect('login')

@csrf_exempt
def photo_record(request):
    photo_id = request.POST.get('photo_id')
    photo = Photo_History.objects.all().filter(id=photo_id)[0]
    photo_path = photo.image
    details = Photo_Details.objects.all().filter(photo=photo_id)
    objects = []
    objects_count = [] 
    for detail in details:
        objects.append(detail.object_name)
        objects_count.append(detail.object_count)
    
    context = {'upload_time':photo.upload_time.strftime("%d, %b %Y - %H:%M"), 'photo_name': request.POST.get('name'), 'photo_path':"media/"+photo_path.name, 'objects': objects, 'values': objects_count}
    # #context = {}
    # return render(request, 'record.html', context)
    return JsonResponse({"message": context})

@csrf_exempt
def comparison_data(request):
    photo_id = request.POST.get('photo_id')
    current_user_id= request.session['user_id']
    photo_name = request.POST.get('name')
    photo = Photo_History.objects.all().filter(id=photo_id)[0]
    photo_path = photo.image
    details = Photo_Details.objects.all().filter(photo=photo_id)
    objects = []
    objects_count = [] 
    for detail in details:
        objects.append(detail.object_name)
        objects_count.append(detail.object_count)
    photo_records = []
    q = "select * from firstApp_Photo_History h where h.photo_id_id in (select p.id from firstApp_Photo p where p.uploader_id = %s and p.name = %s);"
    # photos = Photo_History.objects.raw(q)
    photos = Photo_History.objects.raw(q, [str(Users.objects.filter(username=current_user_id)[0].id), str(photo_name)])
    for p in photos:
        photo_records.append((p.upload_time.strftime("%d, %b %Y - %H:%M"), p.id))
    print("Records: ", photo_records)
    context = {'upload_time':photo.upload_time.strftime("%d, %b %Y - %H:%M"), 'photo_name': photo_name, 'photo_path':"media/"+photo_path.name, 'objects': objects, 'values': objects_count, 'photos': photo_records}
    # #context = {}
    # return render(request, 'record.html', context)
    return JsonResponse({"message": context})

@csrf_exempt
def get_comparison_photo(request):
    photo_id = request.POST.get('photo_id')
    print("Photo ID: ", photo_id)
    photo = Photo_History.objects.all().filter(id=photo_id)[0]
    photo_path = photo.image
    details = Photo_Details.objects.all().filter(photo=photo_id)
    objects = []
    objects_count = [] 
    for detail in details:
        objects.append(detail.object_name)
        objects_count.append(detail.object_count)
    
        context = {'photo_path':"media/"+photo_path.name, 'objects': objects, 'values': objects_count}
    return JsonResponse({"message": context})

def predictImage(request):
    

    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(filePathName)
    testimage = '\imageNetProject'+filePathName
    file_name = get_filepath(fileObj.name)
    print("HERE IT IS: ", testimage)
    img_result, resultant_array, total_objects = show_img(testimage, True)
    cv2.imwrite("media/results/" + file_name, img=img_result)

    photo_history = Photo_History()
    photo_history.image = "results/"+file_name
    
    username = request.POST.get('username')
    if Photo.objects.filter(name = fileObj).exists():
        photo_history.photo_id = Photo.objects.filter(name = fileObj.name, uploader=Users.objects.filter(username=username)[0]).first()
        photo_history.save()
   
    else:
        photo = Photo()
        photo.uploader = Users.objects.get(username = username) 
        photo.name = fileObj.name
        photo.save() 
        photo_history.photo_id = Photo.objects.filter(name = fileObj.name, uploader=Users.objects.filter(username=username)[0]).first()
        photo_history.save()

    # if request.POST.get('image_type') == 'new_photo':
    #     photo = Photo()
    #     photo.uploader = Users.objects.get(username = username) 
    #     photo.name = fileObj.name
    #     photo.save() 
    


    
    
    
    
    # print("File Path: ", file_name)
    # photo.image = "results/"+file_name
    # photo.save()
    
    # photo_history.save()
    for k, v in resultant_array.items():
        photo_details = Photo_Details()
        photo_details.photo = Photo_History.objects.get(image = "results/"+file_name)
        photo_details.object_name = k 
        photo_details.object_count = v
        photo_details.save()
    photos = Photo.objects.all().filter(uploader=Users.objects.filter(username=username)[0])
    print("THIS: ", resultant_array.keys())
    print("SECOND: ", resultant_array.values())
    context = {'ID':username, 'filePathName':"media/results/"+file_name, 'predictedLabel': list(resultant_array.keys()), 'values': list(resultant_array.values())[0], 'clean': (100 - list(resultant_array.values())[0]), 'total_objects': total_objects, 'photos': photos}
    #context = {}
    return render(request, 'index.html', context)


def logout(request):
    del request.session['is_logged']
    return redirect('login')