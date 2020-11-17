from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
import uuid
import pandas as pd
import _thread
import time
from sentiment_analysis_spanish import sentiment_analysis
import redis
import json
from keywords import KeyWordAnalysis

redisConnection = None

def thread1(hash_id):
    df = pd.read_excel('./temp/' + hash_id, header=5)
    comments = df['Comment']
    app.logger.info(comments[2])
    sentiment = sentiment_analysis.SentimentAnalysisSpanish()
    time.sleep(5)
    acumulate = 0
    score = []
    for comment in comments:
        analysis = sentiment.sentiment(comment) * 100
        score.append(analysis)
        if analysis >= 60 : # positive
            acumulate += 2
        elif analysis >= 10 and analysis < 60: # neutro
            acumulate += 1
        elif analysis < 10: # negativo
            acumulate += 0
    app.logger.info(acumulate)
    app.logger.info(len(comments))
    app.logger.info(acumulate / len(comments))

    keyWord = KeyWordAnalysis()
    keywords = keyWord.get_keywords(comments)

    redisConnection.hset(hash_id, 'prediction', ((acumulate / len(comments)) * 100) / 2 )
    redisConnection.hset(hash_id, 'keywords', json.dumps(keywords))
    #df1 = pd.DataFrame({'comment': comments, 'score': score })
    #df1.to_csv('score.csv', index=False)
    #hola prueba 0.01388967
    #odio esto 0.5047717
    #me encanta esta video esta genial 0.8679182

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
            _thread.start_new_thread( thread1, (hash_id, ))
        except:
            print("Error: unable to start threads")
        return redirect("/step-3/" + hash_id, code=302)

@app.route('/step-3/<hash_id>')
def step_3(hash_id):
    analysis = redisConnection.hgetall(hash_id)
    prediction = 0 
    keywords = []
    is_loading = True
    if analysis:
        is_loading = False
        analysis = {key.decode('utf-8'):value.decode('utf-8') for key,value in analysis.items()}
        prediction = analysis['prediction'] 
        keywords = json.loads(analysis['keywords'])
        
    return render_template('step_3.html', prediction=prediction, keywords=keywords, is_loading=is_loading)

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    redisConnection = redis.Redis(host='redis',
                                port=6379,
                                db=0,
                                password='sOmE_sEcUrE_pAsS')
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)