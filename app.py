from flask import Flask,render_template,Response
import cv2
import json

app=Flask(__name__)
camera=cv2.VideoCapture(0)
jsondata = """{
    "faces": [
        {
            "name": "abc xyz", 
            "bbox": [[0,20], [2,60], [3,40], [1,50]]
        }, 
        {
            "name": "def tuv",
            "bbox": [[0,20], [2,60], [3,40], [1,50]]
        }, 

        {
            "name": "mnr jkl", 
           "bbox": [[0,20], [2,60], [3,40], [1,50]]
        }
        ]
}"""
def generate_frames():
    cam_url = "http://192.168.1.201:8080/"
    frameWidth, frameHeight = 640, 480
    
    print("Starting video capture")
    cap = cv2.VideoCapture(cam_url + '/video')
    
    print("Starting video stream reading")
    while True:
           success, frame=cap.read()
           if not success:
               break
           else:
                 faces=json.loads(jsondata)
                 print(type(faces))
                # print(faces)
                #detector=cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
 
                 #faces=detector.detectMultiScale(frame,1.1,7)
 
                 for (x, y, w, h) in faces:
                     cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                  
                # for a in faces['faces']:
                #    print(a)

    
                 ret,buffer=cv2.imencode('.jpg',frame)
                 frame=buffer.tobytes()
                 yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
   

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')





if __name__ == '__main__':
    app.debug = True
    app.run()
