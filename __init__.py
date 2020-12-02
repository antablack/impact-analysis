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

from joblib import dump, load
import numpy as np
import re

redisConnection = None

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def remove_stopswords(comment):
    stop_words = [ "algún", "alguna", "algunas", "alguno", "algunos", "ambos", "ampleamos", "ante", "antes", "aquel", "aquellas", "aquellos", "aqui", "arriba", "atras", "bajo", "bastante", "bien", "cada", "cierta", "ciertas", "cierto", "ciertos", "como", "con", "conseguimos", "conseguir", "consigo", "consigue", "consiguen", "consigues", "cual", "cuando", "dentro", "desde", "donde", "dos", "el", "ellas", "ellos", "empleais", "emplean", "emplear", "empleas", "empleo", "en", "encima", "entonces", "entre", "era", "eramos", "eran", "eras", "eres", "es", "esta", "estaba", "estado", "estais", "estamos", "estan", "estoy", "fin", "fue", "fueron", "fui", "fuimos", "gueno", "ha", "hace", "haceis", "hacemos", "hacen", "hacer", "haces", "hago", "incluso", "intenta", "intentais", "intentamos", "intentan", "intentar", "intentas", "intento", "ir", "la", "largo", "las", "lo", "los", "mientras", "mio", "modo", "muchos", "muy", "nos", "nosotros", "otro", "para", "pero", "podeis", "podemos", "poder", "podria", "podriais", "podriamos", "podrian", "podrias", "por", "por qué", "porque", "primero", "puede", "pueden", "puedo", "quien", "sabe", "sabeis", "sabemos", "saben", "saber", "sabes", "ser", "si", "siendo", "sin", "sobre", "sois", "solamente", "solo", "somos", "soy", "su", "sus", "también", "teneis", "tenemos", "tener", "tengo", "tiempo", "tiene", "tienen", "todo", "trabaja", "trabajais", "trabajamos", "trabajan", "trabajar", "trabajas", "trabajo", "tras", "tuyo", "ultimo", "un", "una", "unas", "uno", "unos", "usa", "usais", "usamos", "usan", "usar", "usas", "uso", "va", "vais", "valor", "vamos", "van", "vaya", "verdad", "verdadera", "verdadero", "vosotras", "vosotros", "voy", "yo", "él", "ésta", "éstas", "éste", "éstos", "última", "últimas", "último", "últimos", "a", "añadió", "aún", "actualmente", "adelante", "además", "afirmó", "agregó", "ahí", "ahora", "al", "algo", "alrededor", "anterior", "apenas", "aproximadamente", "aquí", "así", "aseguró", "aunque", "ayer", "buen", "buena", "buenas", "bueno", "buenos", "cómo", "casi", "cerca", "cinco", "comentó", "conocer", "consideró", "considera", "contra", "cosas", "creo", "cuales", "cualquier", "cuanto", "cuatro", "cuenta", "da", "dado", "dan", "dar", "de", "debe", "deben", "debido", "decir", "dejó", "del", "demás", "después", "dice", "dicen", "dicho", "dieron", "diferente", "diferentes", "dijeron", "dijo", "dio", "durante", "e", "ejemplo", "ella", "ello", "embargo", "encuentra", "esa", "esas", "ese", "eso", "esos", "está", "están", "estaban", "estar", "estará", "estas", "este", "esto", "estos", "estuvo", "ex", "existe", "existen", "explicó", "expresó", "fuera", "gran", "grandes", "había", "habían", "haber", "habrá", "hacerlo", "hacia", "haciendo", "han", "hasta", "hay", "haya", "he", "hecho", "hemos", "hicieron", "hizo", "hoy", "hubo", "igual", "indicó", "informó", "junto", "lado", "le", "les", "llegó", "lleva", "llevar", "luego", "lugar", "más", "manera", "manifestó", "mayor", "me", "mediante", "mejor", "mencionó", "menos", "mi", "misma", "mismas", "mismo", "mismos", "momento", "mucha", "muchas", "mucho", "nada", "nadie", "ni", "ningún", "ninguna", "ningunas", "ninguno", "ningunos", "no", "nosotras", "nuestra", "nuestras", "nuestro", "nuestros", "nueva", "nuevas", "nuevo", "nuevos", "nunca", "o", "ocho", "otra", "otras", "otros", "parece", "parte", "partir", "pasada", "pasado", "pesar", "poca", "pocas", "poco", "pocos", "podrá", "podrán", "podría", "podrían", "poner", "posible", "próximo", "próximos", "primer", "primera", "primeros", "principalmente", "propia", "propias", "propio", "propios", "pudo", "pueda", "pues", "qué", "que", "quedó", "queremos", "quién", "quienes", "quiere", "realizó", "realizado", "realizar", "respecto", "sí", "sólo", "se", "señaló", "sea", "sean", "según", "segunda", "segundo", "seis", "será", "serán", "sería", "sido", "siempre", "siete", "sigue", "siguiente", "sino", "sola", "solas", "solos", "son", "tal", "tampoco", "tan", "tanto", "tenía", "tendrá", "tendrán", "tenga", "tenido", "tercera", "toda", "todas", "todavía", "todos", "total", "trata", "través", "tres", "tuvo", "usted", "varias", "varios", "veces", "ver", "vez", "y", "ya"]
    stop_words = set(stop_words)
    comment = ' '.join([word for word in comment.split() if word not in stop_words])
    comment = comment.replace('.', '')
    comment = comment.replace(',', '')
    comment = comment.replace(':', '')
    comment = comment.replace(';', '')
    return deEmojify(comment)

def normalize(comments):
    comments_str = []
    for comment in comments:
        comment = str(comment).lower().strip()
        comment = remove_stopswords(comment)
        comments_str.append(comment)
    return comments_str

def thread1(hash_id):
    log_model = load('./model/model.joblib') 
    vectorizer = load('./model/vectorizer.joblib') 
    
    df = pd.read_excel('./temp/' + hash_id, header=5)
    comments = df['Comment']
    app.logger.info(comments[1])
    comments = normalize(comments)
    app.logger.info(comments[1])
    #comments = ['odio esto', 'no me interesa', 'me encanto', '....'] 
    features = vectorizer.transform(comments)
    features_nd = features.toarray()
    y_pred = log_model.predict(features)

    acumulate = 0
    score = []
    for y in y_pred:
        acumulate += y

    app.logger.info(acumulate)
    app.logger.info(len(comments))
    app.logger.info(acumulate / len(comments))

    keyWord = KeyWordAnalysis()
    keywords = keyWord.get_keywords(comments)

    redisConnection.hset(hash_id, 'prediction', (acumulate / len(comments)) * 100)
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