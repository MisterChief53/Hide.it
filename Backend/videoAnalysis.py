import cv2
import numpy as np

video = cv2.VideoCapture('Video/video.mp4')

width_frame = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height_frame = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

fps = int(video.get(cv2.CAP_PROP_FPS))

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

video_out = cv2.VideoWriter(f'Video/Output/video.mp4', fourcc, fps, (width_frame, height_frame))

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


print(detected_classes)

selected_label = 'pottedplant'
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
