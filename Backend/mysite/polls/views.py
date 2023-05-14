from django.http import HttpResponse
import os
import requests
import time

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def upload_video(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['video_file']
        # do something with the uploaded file
        return render(request, 'video_uploaded.html')
    return render(request, 'upload_video.html')


def check_for_specific_file(directory_path, file_name):
    """
    Check if a specific file is in a directory.
    Returns True if the file exists, False otherwise.
    """
    file_path = os.path.join(directory_path, file_name)
    return os.path.exists(file_path)

def notify_api():
    """
    Notify the Django API that the specific file has been found.
    """
    url = 'http://localhost:8000/polls/media/'
    response = requests.post(url)
    return response.status_code

def main():
    directory_path = 'http://localhost:8000/polls/media/'
    file_name = 'try.txt'
    file_found = False
    
    while not file_found:
        if check_for_specific_file(directory_path, file_name):
            notify_api()
            file_found = True
        else:
            time.sleep(10) # sleep for 60 seconds before checking again
