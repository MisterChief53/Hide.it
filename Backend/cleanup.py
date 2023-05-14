import os


os.remove('Video/video.mp4')
os.remove('Video/Output/video.mp4')

frames_path = 'Frames'

for filename in os.listdir(frames_path):
    file_path = os.path.join(frames_path, filename)

    if os.path.isfile(file_path) and filename != '.gitkeep':
        os.remove(file_path)