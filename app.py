#importar flask
from flask import Flask, render_template

#Se crea la imnstancia de la app Flask
app = Flask(__name__)

#Se define ruta de la app
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

if __name__ == '__main__': 
    app.run(debug=True)
