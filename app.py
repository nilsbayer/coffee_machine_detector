from flask import Flask, render_template, request, jsonify, url_for, Response
import cv2
import torch
import numpy as np

app = Flask(__name__)

global search_results
search_results = []

model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/last.pt', force_reload=True)

def gen_frames():
    camera = cv2.VideoCapture(1)
    global search_results
    while True:
        success, frame = camera.read()

        result = model(frame)
        search_results = result.xyxy[0]

        # if len(search_results) > 0 and search_results[0][-2].item() > .55:
        #     print(search_results)
        
        frame = np.squeeze(result.render())

        if success:
            try:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                print("****************** ERROR CAMERA ************************", e)

        else:
            print("No frames received from camera.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/detection", methods=["POST"])
def detection_send():
    global search_results
    results_to_send = []
    for result in search_results:
        if result[-2].item() > .40:
            possible_machines = {
                15.0: {
                        "name": "Delonghi Dedica",
                        "info_text": "Die klassische Einsteiger-Maschine. Starke Leistung für einen fairen Preis.",
                        "img_path": "../static/data/images/test10.png",
                        "link": "delonghi-dedica",
                    }
            }
            machine = possible_machines.get(result[-1].item())
            if machine not in results_to_send:
                results_to_send.append(machine)

    num_machines_detected = len(results_to_send)

    return jsonify({
        "data_length": num_machines_detected,
        "items": results_to_send
    })

@app.route("/explore/delonghi-dedica")
def explore():
    return render_template("dedica.html")


if __name__ == "__main__":
    app.run(debug=True)