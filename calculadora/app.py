from flask import Flask,render_template
from calculadora import calcular

app = Flask(__name__)

@app.route("/")
def calculadora():
    return render_template('calculadora.html', etapas = '', resultado ='')

@app.route('/calcular', methods=['POST'])
def calcular_route():
    return calcular()





if __name__ == "__main__":
    app.run(debug=True)



