#!/usr/bin/env python

import time
from flask import Flask, render_template, Response, request, jsonify
from sqlalchemy import create_engine
from app import VideoStream

app = Flask(__name__)
mimetype = 'multipart/x-mixed-replace; boundary=frame'
engine = create_engine('sqlite:///db.sqlite')


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
        return Response(gen(VideoStream()), mimetype=mimetype)
    except Exception as err:
        print(err)

@app.route('/frame_key_log', methods=['POST'])
def video_key_log():
    key = request.form['key']
    width = request.form['width']
    height = request.form['height']
    print(request.files.get('frame'))

    return jsonify(key=key)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)