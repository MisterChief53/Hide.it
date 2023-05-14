import cv2
import numpy as np
import moviepy.editor as mp
from flask import Flask, render_template, url_for, request, redirect, send_file, send_from_directory, jsonify
import requests
import os
import time

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'Video'
videoNotUploaded = True
classSelected = False
frame_count = 0
objects_overall = []
flag = False
detected_classes = []
needDelete = False
#width_frame = 0
#height_frame = 0
#fps = 0
noVideo = False
@app.route('/', methods=['GET', 'POST'])

def index():
    global flag
    global detected_classes
    global classSelected
    global needDelete
    videoNotUploaded = os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], 'video.mp4'))
    if videoNotUploaded and flag == False:
        detected_classes = process_video()
        #process_videoPt2('person')
        classSelected = True
        #videoNotUploaded = False
        flag = True
    if request.method == 'POST' and request.form.get('form_name') == 'classesForm':
        selected_label = request.form.get('item')
        print(f"selected label: {selected_label}")
        process_videoPt2(selected_label)
        classSelected = True
        detected_classes = []
        detected_classes.append(selected_label)
        return render_template('upload.html', videoNotUploaded=not videoNotUploaded, detected_classes=detected_classes, classSelected=classSelected)
    
    return render_template('upload.html', videoNotUploaded=not videoNotUploaded, detected_classes=detected_classes, classSelected=classSelected)

@app.route('/landing', methods=['GET', 'POST'])
    
def landing():
    global flag
    global detected_classes
    global classSelected
    global needDelete
    if needDelete:
        os.remove('Video/video.mp4')
        os.remove('Video/Output/video.mp4')
        os.remove('Video/Output/final_video.mp4')

        frames_path = 'Frames'

        for filename in os.listdir(frames_path):
            file_path = os.path.join(frames_path, filename)

            if os.path.isfile(file_path) and filename != '.gitkeep':
                os.remove(file_path)
        classSelected = False
        flag = False
        needDelete = False
    #return render_template('Any.html', result=result, imagePath=imagePath)
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        video_file = request.files['file']
        if video_file:
            filename = 'video.mp4'
            video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('index'))

@app.route('/videos/<path:filename>', methods=['GET', 'POST'])
def serve_video(filename):
    directory = 'Video'
    return send_from_directory(directory, filename)

@app.route('/finalVideos/<path:filename>', methods=['GET', 'POST'])
def serve_final_video(filename):
    directory = 'Video/Output'
    return send_from_directory(directory, filename)

@app.route('/delete_video', methods=['POST'])
def delete_video():
    print("delete_video called")
    filename = request.json['filename']
    file_path = os.path.join("Video/", filename)


    if os.path.isfile('Video/Output/video.mp4'):
        os.remove('Video/Output/video.mp4')
        return jsonify({'message': 'Video deleted successfully'})

    frames_path = 'Frames'

    for filename in os.listdir(frames_path):
        file_path = os.path.join(frames_path, filename)

        if os.path.isfile(file_path) and filename != '.gitkeep':
            os.remove(file_path)

    if os.path.isfile(file_path):
        os.remove(file_path)
        return jsonify({'message': 'Video deleted successfully'})
    else:
        return jsonify({'message': 'Video not found'})
    
    

def process_video():
    global frame_count
    global objects_overall
    video = cv2.VideoCapture('Video/video.mp4')

    #width_frame = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    #height_frame = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    #fps = int(video.get(cv2.CAP_PROP_FPS))

    frame_count = 0

    while True:
        ret, frame = video.read()

        if not ret:
            break

        cv2.imwrite(f'Frames/frame{frame_count}.jpg', frame)

        frame_count += 1

    video.release()

    #set up video codec
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    #load yolo trained on cocos
    net = cv2.dnn.readNetFromDarknet('yolov3-spp.cfg', 'yolov3-spp.weights')

    with open('coco.names', 'r') as f:
        classes = [line.strip() for line in f.readlines()]


    detected_classes = set()

    objects_overall = []

    for i in range(frame_count):
        frame = cv2.imread(f'Frames/frame{i}.jpg')

        #processing!

        (h, w) = frame.shape[:2] ##just to make sure

        objects = []

        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)

        net.setInput(blob)

        output_layers = net.getUnconnectedOutLayersNames()
        layer_outputs = net.forward(output_layers)

        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = scores.argmax()
                confidence = scores[class_id]

                if confidence > 0.5:
                    box = detection[:4] * np.array([w,h,w,h])
                    (centerX, centerY, width, height) = box.astype('int')
                    x = int(centerX - (width/2))
                    y = int(centerY - (height/2))
                    objects.append((classes[class_id], confidence, (x,y, int(width), int(height))))

        objects_overall.append(objects)

        for obj in objects:
            if obj[1] > 0.5:
                if obj[0] not in detected_classes:
                    detected_classes.add(obj[0])
    return detected_classes

def process_videoPt2(selected_label):
    global frame_count
    print(f'frame_count: {frame_count}')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoCapture('Video/video.mp4')
    width_frame = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height_frame = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = int(video.get(cv2.CAP_PROP_FPS))
    video.release()

    video_out = cv2.VideoWriter(f'Video/Output/video.mp4', fourcc, fps, (width_frame, height_frame))
    for i in range(frame_count):
        frame = cv2.imread(f'Frames/frame{i}.jpg')

        #processing!

        for obj in objects_overall[i]:
            #label = f'{obj[0]}: {obj[1]:.2f}'

            (x,y,w,h) = obj[2]
            #cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            #cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), -1)
            
            if obj[0] == selected_label:
                if x >= 0 and y >= 0 and x+w <= width_frame and y+h <= height_frame:
                    roi = frame[y:y+h, x:x+w]
                    print(f"roi shape: {roi.shape}")
                    print(f"roi empty: {roi.size == 0}")
                    blurred_roi = cv2.GaussianBlur(roi, (251,251), 0)
                    frame[y:y+h, x:x+w] = blurred_roi
            
            
            #cv2.putText(frame,label,(x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),2)

        video_out.write(frame)
        

    video_out.release()

    video_no_audio = mp.VideoFileClip("Video/Output/video.mp4")
    video_with_audio = mp.VideoFileClip("Video/video.mp4")

    audio = video_with_audio.audio

    final_video = video_no_audio.set_audio(audio)

    final_video.write_videofile("Video/Output/final_video.mp4")