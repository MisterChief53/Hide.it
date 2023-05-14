# Hide.it

Hide.it is an automatic video censorship system that analyzes your video looking for known objects, asks you which one you want to censor, and then gives you back
a censored version of your own video.

# Tecnologies used:
- OpenCV
- YOLOv3
- Python
- DJango
- Bootstrap
- Javascript
- COCO dataset

# How to use it:

# Installation and setup
1. Clone the repository
2. Install the requirements. Recommended to use a virtual environment and install the requirements.txt file
3. Download the YOLOv3 weights from [here](https://pjreddie.com/media/files/yolov3.weights) and place them in the Backend folder of the project
4. Run the server with `python manage.py runserver`
5. Go to the url and use the app