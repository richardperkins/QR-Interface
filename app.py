from flask import Flask, render_template, url_for, Response, send_file
from webcam import Webcam
import time
from random import randrange
import cv2
from PIL import Image
import qrcode
from io import StringIO, BytesIO
from playsound import playsound

app = Flask(__name__)

video_stream = Webcam()
tid = ""

def play_beep():
	playsound("C:\\Users\\BrawnSwagger\\Source\\Repos\\QR-Interface\\beep.wav")

@app.route('/')
def index():
	title = "Title"
	tid = get_new_tid()
	return render_template('index.html', **locals())

def generate_camera_frame(camera):
	detector = cv2.QRCodeDetector()
	while True:
		video_stream.refresh()
		data = video_stream.get_qr_code()
		img = video_stream.get_frame()

		if data:
			play_beep()
			print(data)

		yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n')
		#time.sleep(1)

@app.route('/video_feed')
def video_feed():
	return Response(generate_camera_frame(video_stream),
		mimetype="multipart/x-mixed-replace; boundary=frame")
@app.route('/qr_code')
def qr_code():
	globals()['tid']
	img_io = BytesIO()
	qr = qrcode.make(tid)
	qr.save(img_io, "JPEG", quality=70)
	img_io.seek(0)
	return send_file(img_io, mimetype="image/jpeg")

def get_new_tid():
	globals()["tid"] = ""
	for x in range(6):
		globals()["tid"] += str(randrange(10))
	return globals()["tid"]