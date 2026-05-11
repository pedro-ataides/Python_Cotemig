from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Acesse <a href="/decorator">/decorator</a> para ver a explicação.'

@app.route('/decorator')
def explicar_decorator():
    explicacao = """
    <p>Conceito de Decorator em Python</p>
    
    <p>1. O que é?</p>
    <p>Um <b>decorator</b> (de é uma função que envolve outra função para estender ou alterar o seu comportamento, 
    sem modificar permanentemente o código da fcorador)unção original. No Python, eles são identificados pelo símbolo <b>@</b>.</p>
    
    <p>2. Para que serve?</p>
    <p>Serve para reaproveitar lógica de forma limpa. É muito usado para:</p>
    <ul>
        <li>Logs e monitoramento.</li>
        <li>Controle de autenticação (verificar se usuário está logado).</li>
        <li>Cache de dados.</li>
        <li>Definição de rotas em frameworks web.</li>
    </ul>

    <p>3. Como é utilizado no Flask (Exemplo: @app.route)</p>
    <p>No Flask, o decorator <code>@app.route("/")</code> é fundamental. Ele "embrulha" a função que você criou e diz ao Flask: 
    "Sempre que alguém acessar esta URL no navegador, execute esta função específica e retorne o resultado."</p>
    
    <p>Sem o decorator, o Flask não saberia qual função disparar para cada endereço digitado.</p>
    """
    return explicacao

if __name__ == '__main__':
    app.run(debug=True)