from django.http import HttpResponse
import subprocess
from django.http import JsonResponse
import os
import requests
import time

from . import videoAnalysis

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

#def upload_video(request):
#    if request.method == 'POST':
#        uploaded_file = request.FILES['video_file']
#        # do something with the uploaded file
#        return render(request, 'video_uploaded.html')
#    return render(request, 'upload_video.html')

#def lookForVideo(request):
#    directory_path = 'media/'
#    file_name = 'try.txt'
#    
#    file_found = False
##    
#    while not file_found:
#        file_path = './media/video.txt'
#        if not os.path.exists(file_path):
#            return HttpResponse("There is not a video")
#            # Perform an action, such as sleeping for a few seconds
#            time.sleep(10)
#        else:
#            file_found = True
#
#
#    return HttpResponse("There is a video")



def process_video(request):
    # procesar el video subido aquí

    # ejecutar el archivo .py
    subprocess.run(['python', '/ruta/a/tu/archivo.py'])

    # devolver la información del nuevo video en una respuesta JSON
    nuevo_video = {
        'titulo': 'Nuevo video',
        'ruta': '/ruta/al/nuevo/video.mp4'
    }
    return JsonResponse(nuevo_video)

def postClassesArray(request):
    return JsonResponse({
            'status':'ok',
            'array': videoAnalysis.detected_classes,
        })
