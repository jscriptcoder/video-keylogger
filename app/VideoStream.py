import cv2

class VideoStream():
    def __init__(self):
        self.video = cv2.VideoCapture('app/Atari-2600_Space-Invaders.mp4')

    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, frame = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()