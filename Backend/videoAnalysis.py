import cv2

video = cv2.VideoCapture('Video/video.mp4')

width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

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
net = cv2.dnn.readNetFromDarknet('yolo3-spp.cfg', 'yolov3-spp.weights')

with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

video_out = cv2.VideoWriter(f'Video/Output/video.mp4', fourcc, fps, (width, height))

for i in range(frame_count):
    frame = cv2.imread(f'Frames/frame{i}.jpg')

    #processing!

    video_out.write(frame)

video_out.release()