from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
import uuid
import pandas as pd
import _thread
import time

def thread1(hash_id):
    df = pd.read_excel('comments.xlsx', header=5)
    comments = df['Comment']
    print(comments[0])
    time.sleep(5)



app = Flask(__name__)

@app.route('/')
def step_1():
    return render_template('step_1.html')

@app.route('/step-2', methods=['GET', 'POST'])
def step_2():
    if request.method == 'GET':
        return render_template('step_2.html')
    else:
        hash_id = str(uuid.uuid4())
        f = request.files['file']
        f.save(os.getcwd() + '/temp/' + hash_id)
        try:
            #_thread.start_new_thread( thread1, (hash_id, ))
        except:
            print("Error: unable to start threads", sys.exc_info()[0])
        return redirect("/step-3", code=302)

@app.route('/step-3')
def step_3():
    return render_template('step_3.html')

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)