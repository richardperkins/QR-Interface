import cv2

class Webcam:


	def __init__(self):
		self.video = cv2.VideoCapture(0)
		self.detector = cv2.QRCodeDetector()
	
	def __del__(self):
		self.video.release()

	def refresh(self):
		self.frame = self.video.read()[1]
		return self.frame

	def get_frame(self):
		ret, jpeg = cv2.imencode('.jpg', self.frame)
		jpeg = jpeg.tobytes()

		return jpeg

	def get_qr_code(self):
		try:
			data, bbox, straght_qrcode = self.detector.detectAndDecode(self.frame)
		except:
			print("Error reading QR from webcam")
			return
		else:
			return data