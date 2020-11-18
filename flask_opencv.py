import cv2
import time
import threading

from flask import Response
from flask import Flask
from flask import render_template
from flask import request, send_from_directory

screen_update_frame_rate = 25
capture = None
outputFrame = None

rtsp_link = 'rtsp://127.0.0.1:8080/h264_pcm.sdp'

def generate_response():    
    if outputFrame is None:
        return
    sleep_delay = 1/screen_update_frame_rate
    while True:		
        l=outputFrame.__len__()
        if outputFrame is None or l==0:
            continue              
        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)        
        if not flag:
            continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')
        time.sleep(sleep_delay)

web_server = Flask(__name__)
@web_server.route("/")
def index():
	return render_template("index.html")

@web_server.route('/dist/<path:path>')
def send_js(path):
    return send_from_directory('templates/dist', path)

@web_server.route("/video_feed")
def video_feed():	
	return Response(generate_response(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

def update():
    global capture,outputFrame
    # Read the next frame from the stream in a different thread
    while True:
        if capture.isOpened():                
            (status, frame) = capture.read()
            if status==True:
                outputFrame = frame.copy()                                                   
            else:
                check = False
                while not check:
                    capture = cv2.VideoCapture(rtsp_link)
                    (status, frame) = capture.read()                     
                    if status:
                        check = True
                    else:
                        time.sleep(0.2)                                


def run_server():
    web_server.run(host="0.0.0.0", port="4444", debug=True,threaded=True, use_reloader=False)

if __name__ == '__main__':    
    capture = cv2.VideoCapture(rtsp_link)
    web_server_thread = threading.Thread(target = run_server)    
    web_server_thread.start() 
    frame_update_thread = threading.Thread(target=update, args=())    
    frame_update_thread.start()
    input("Press any key to exit...")
    