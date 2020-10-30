#!/usr/bin/env python

import cv2
import time
from datetime import datetime
from flask import Flask, render_template, Response, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./key_frames.db'
db = SQLAlchemy(app)


class KeyFrameModel(db.Model):
    __tablename__ = 'key_frame'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)
    filename = db.Column(db.String(50))
    key = db.Column(db.Integer)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    frame = db.Column(db.LargeBinary)

db.create_all() # creates db and table

class VideoStream():
    def __init__(self):
        self.video = cv2.VideoCapture('app/Atari-2600_Space-Invaders.mp4')

    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, frame = self.video.read()
        if success:
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        else:
            # rewind
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)


@app.route('/')
def index():
    return render_template('index.html')

def gen(video):
    while True:
        frame = video.get_frame()
        if frame is not None:
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(.01)

@app.route('/video_feed')
def video_feed():
    try:
        return Response(gen(VideoStream()), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as err:
        print(err)

@app.route('/frame_key_log', methods=['POST'])
def video_key_log():
    key = request.form['key']
    width = request.form['width']
    height = request.form['height']
    frame = request.files['frame']
    filename = frame.filename

    keyFrame = KeyFrameModel(filename=filename, 
                             key=key, 
                             width=width, 
                             height=height, 
                             frame=frame.read())
    
    db.session.add(keyFrame)
    db.session.commit()

    return jsonify(filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)