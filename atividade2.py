from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return 'Acesse <a href="/decorator">/decorator</a> para ver a explicação.'


@app.route("/decorator")
def explicacao():
    explicacao = """
<h1>PEDRO ATAIDES</h1>
<p>Guaicurus, Belo Horizonte, MG, 30 000 000 |  Aluno@cotemig.com.br | 6969-6969</p>
<p>OBJETIVO <br>Estágio ou emprego na área de TI </p>
<p>HABILIDADES E COMPETÊNCIAS <br> Eletricidade – Básica</p>

    <ul>
        <li>Proteção / Segurança </li>
        <li>Dimensionamento </li>
        <li>Manutenção e testes </li>
        <li>Multímetro digital</li>
    </ul>
<p>Hardware – Intermediário</p>
    <ul>
        <li>Montagem e manutenção</li>
        <li>Dimensionamento / Adequação </li>
        <li>Instalação e configuração </li>
        <li>Consultoria</li>
    </ul>

<p>EXPERIÊNCIA<br>Nenhuma😂</p>

<p>EDUCAÇÃO <br> COLÉGIO E FACULDADE COTEMIG, BELO HORIZONTE MG <br> TÉCNICO EM INFORMÁTICA GERENCIAL – EM CURSO 3ª SÉRIE</p>


<p>COMUNICAÇÃO<br> Debate sobre tecnologias emergentes concorrentes – Apple x Samsung <br> Auditório – Faculdade Cotemigs</p>



    """
    return explicacao


if __name__ == "__main__":
    app.run(debug=True)
