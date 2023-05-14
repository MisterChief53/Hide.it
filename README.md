# Hide.it
![Logo](https://i.imgur.com/WQwHIEi.png)

Hide.it is an automatic video censorship system that analyzes your video looking for known objects, asks you which one you want to censor, and then gives you back
a censored version of your own video.

# Tecnologies used:
- OpenCV
- YOLOv3
- Python
- Flask
- Bootstrap
- Javascript
- COCO dataset

# How to use it:
1. Upload a video
2. Wait for the analysis to finish
3. Select the object you want to censor
4. Wait for the censorship to finish
5. Download the censored video


# Installation and setup
1. Clone the repository
2. Install the requirements. Recommended to use a virtual environment and install the requirements.txt file
3. Download the YOLOv3 weights from [here](https://pjreddie.com/media/files/yolov3.weights) and place them in the Backend folder of the project
4. Run the server with `flask --app videoAnalysis.py run`
5. Go to the url provided by flask and use the app