from sklearn.feature_extraction.text import CountVectorizer
import re

class KeyWordAnalysis:
    def __init__(self):
        print("Analysis Instance")

    def pre_process(self, text):
        text = text.lower()
        text = re.sub("(\\d|\\W)+", " ", text)
        return text
    
    def get_stopwords(self):
        stop_words = [ "algún", "alguna", "algunas", "alguno", "algunos", "ambos", "ampleamos", "ante", "antes", "aquel", "aquellas", "aquellos", "aqui", "arriba", "atras", "bajo", "bastante", "bien", "cada", "cierta", "ciertas", "cierto", "ciertos", "como", "con", "conseguimos", "conseguir", "consigo", "consigue", "consiguen", "consigues", "cual", "cuando", "dentro", "desde", "donde", "dos", "el", "ellas", "ellos", "empleais", "emplean", "emplear", "empleas", "empleo", "en", "encima", "entonces", "entre", "era", "eramos", "eran", "eras", "eres", "es", "esta", "estaba", "estado", "estais", "estamos", "estan", "estoy", "fin", "fue", "fueron", "fui", "fuimos", "gueno", "ha", "hace", "haceis", "hacemos", "hacen", "hacer", "haces", "hago", "incluso", "intenta", "intentais", "intentamos", "intentan", "intentar", "intentas", "intento", "ir", "la", "largo", "las", "lo", "los", "mientras", "mio", "modo", "muchos", "muy", "nos", "nosotros", "otro", "para", "pero", "podeis", "podemos", "poder", "podria", "podriais", "podriamos", "podrian", "podrias", "por", "por qué", "porque", "primero", "puede", "pueden", "puedo", "quien", "sabe", "sabeis", "sabemos", "saben", "saber", "sabes", "ser", "si", "siendo", "sin", "sobre", "sois", "solamente", "solo", "somos", "soy", "su", "sus", "también", "teneis", "tenemos", "tener", "tengo", "tiempo", "tiene", "tienen", "todo", "trabaja", "trabajais", "trabajamos", "trabajan", "trabajar", "trabajas", "trabajo", "tras", "tuyo", "ultimo", "un", "una", "unas", "uno", "unos", "usa", "usais", "usamos", "usan", "usar", "usas", "uso", "va", "vais", "valor", "vamos", "van", "vaya", "verdad", "verdadera", "verdadero", "vosotras", "vosotros", "voy", "yo", "él", "ésta", "éstas", "éste", "éstos", "última", "últimas", "último", "últimos", "a", "añadió", "aún", "actualmente", "adelante", "además", "afirmó", "agregó", "ahí", "ahora", "al", "algo", "alrededor", "anterior", "apenas", "aproximadamente", "aquí", "así", "aseguró", "aunque", "ayer", "buen", "buena", "buenas", "bueno", "buenos", "cómo", "casi", "cerca", "cinco", "comentó", "conocer", "consideró", "considera", "contra", "cosas", "creo", "cuales", "cualquier", "cuanto", "cuatro", "cuenta", "da", "dado", "dan", "dar", "de", "debe", "deben", "debido", "decir", "dejó", "del", "demás", "después", "dice", "dicen", "dicho", "dieron", "diferente", "diferentes", "dijeron", "dijo", "dio", "durante", "e", "ejemplo", "ella", "ello", "embargo", "encuentra", "esa", "esas", "ese", "eso", "esos", "está", "están", "estaban", "estar", "estará", "estas", "este", "esto", "estos", "estuvo", "ex", "existe", "existen", "explicó", "expresó", "fuera", "gran", "grandes", "había", "habían", "haber", "habrá", "hacerlo", "hacia", "haciendo", "han", "hasta", "hay", "haya", "he", "hecho", "hemos", "hicieron", "hizo", "hoy", "hubo", "igual", "indicó", "informó", "junto", "lado", "le", "les", "llegó", "lleva", "llevar", "luego", "lugar", "más", "manera", "manifestó", "mayor", "me", "mediante", "mejor", "mencionó", "menos", "mi", "misma", "mismas", "mismo", "mismos", "momento", "mucha", "muchas", "mucho", "nada", "nadie", "ni", "ningún", "ninguna", "ningunas", "ninguno", "ningunos", "no", "nosotras", "nuestra", "nuestras", "nuestro", "nuestros", "nueva", "nuevas", "nuevo", "nuevos", "nunca", "o", "ocho", "otra", "otras", "otros", "parece", "parte", "partir", "pasada", "pasado", "pesar", "poca", "pocas", "poco", "pocos", "podrá", "podrán", "podría", "podrían", "poner", "posible", "próximo", "próximos", "primer", "primera", "primeros", "principalmente", "propia", "propias", "propio", "propios", "pudo", "pueda", "pues", "qué", "que", "quedó", "queremos", "quién", "quienes", "quiere", "realizó", "realizado", "realizar", "respecto", "sí", "sólo", "se", "señaló", "sea", "sean", "según", "segunda", "segundo", "seis", "será", "serán", "sería", "sido", "siempre", "siete", "sigue", "siguiente", "sino", "sola", "solas", "solos", "son", "tal", "tampoco", "tan", "tanto", "tenía", "tendrá", "tendrán", "tenga", "tenido", "tercera", "toda", "todas", "todavía", "todos", "total", "trata", "través", "tres", "tuvo", "usted", "varias", "varios", "veces", "ver", "vez", "y", "ya"]
        stop_set = set(m.strip() for m in stop_words)
        return frozenset(stop_set)
    
    def get_keywords(self, df_text):
        stop_words = self.get_stopwords()

        df_text = map(lambda text: self.pre_process(text), df_text)
        df_text = list(df_text)

        cv = CountVectorizer(max_df=0.85, stop_words=stop_words, max_features=10000)
        word_count_vector = cv.fit_transform(df_text)

        words = list(cv.vocabulary_.keys())[:50]
        return words


#df_text = [
#    'El ONE PIECE es 100% real no feikEso me mato de risa jajajaja pero One Piece es muy triste y su guerra supera la de naruto XD gracias por subirlo',
#    'Justo ayer vi uno de tus vídeos y, ya soy seguidor tuyo, contrario a otros, me dan ganas de ver los animes por la forma tan fascinante en que los resumes,🤣🤣🤣🤣sigue así 💪💪💪,',
#    'Siempre tuve curiosidad por one peace, pero la verdad me pareció muy tedioso, llegué hasta el cap 30...😌 😌 😌 Cuando quiae volver a verlo ya iba por el cap 900 y dije nica lo veo, asi queee gracias por el mega resumen 👌👌😜']


#keyWord = KeyWordAnalysis()

#print(keyWord.get_keywords(df_text))
