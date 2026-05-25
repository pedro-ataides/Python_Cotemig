import requests
from flask import Flask,render_template,request

def calcular():
    num1 = float(request.form['num1'])
    num2 = float(request.form['num2'])
    operacao = float(request.form['operacao'])
    
    if operacao == '+':
        resultado = num1 + num2
        etapas = f'{num1} + {num2} = {resultado}'
    elif operacao == '-':
        resultado = num1 - num2
        etapas = f'{num1} - {num2} = {resultado}'
    elif operacao =='*':
        resultado = num1 * num2
        etapas = f'{num1} * {num2} = {resultado}'
    elif operacao =='/':
        if num2 != 0:
         resultado = num1 / num2
         etapas = f'{num1} / {num2} = {resultado}'
        else:
            resultado = "erro divisão por zero"
            etapas = "Nao é possivel dividir por zero"
    else:
        resultado = "Operaçao invaliada"
        etapas = "Operaçao selecionada invalida"
    
    
    
    
    
    return render_template('calculadora.html', etapas = etapas, resultado = resultado)
    
    
    
    