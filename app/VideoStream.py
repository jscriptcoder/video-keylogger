import cv2

class VideoStream():
    def __init__(self):
        self.video = cv2.VideoCapture('Atari-2600_Space-Invaders.mp4')

    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()