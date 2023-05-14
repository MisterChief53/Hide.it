from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def upload_video(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['video_file']
        # do something with the uploaded file
        return render(request, 'video_uploaded.html')
    return render(request, 'upload_video.html')
