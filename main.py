import re
import numpy as np
import array
from fastapi import FastAPI


##A maneira de calcular é simples. Os dois dígitos no final são os dígitos verificadores. Sabemos isso com as
#seguintes contas:
#  . Pegue os 9 primeiros dígitos do CPF, multiplique pelos números de 2 a 10 em ordem decrescente
#Então no CPF 793.224.651-23 a conta seria:
#  7*10 + 9*9 + 3*8 + 2*7 + 2*6 + 4*5 + 6*4 + 5*3 + 1*2
#Agora multiplique o resultasdo por 10 e divida por 11. Se o resto da divisão bater com o primeiro dígito, ele
#está validado.
#(262*10) %% 11 == 2 # primeiro dígito é válido
## [1] TRUE
#. Pegue os 10 primeiros números e multiplique pelos números de 11 a 2 em ordem decrescente
#7*11 + 9*10 + 3*9 + 2*8 + 2*7 + 4*6 + 6*5 + 5*4 + 1*3 + 2*2
#Agora multiplique o resultado por 10 e divida por 11. Se o resto da divisão bater com o segundo dígito, ele
#está validado.
#(305*10) %% 11 == 3
## [1] TRUE

app = FastAPI()

@app.get("/")
def home():
    return "bem vindo a minha app de validacao de cpf"

@app.get("/validacao/{cpf}")
def validacpf(cpf: str):
    # pegando o input e mantendo so os numeros
    cpf_apenas_numeros = re.sub("[^0-9]", "", cpf)
    # transformando em nparray para fazer operacoes vetorizadas
    cpf_apenas_numeros = np.array(list(map(int, cpf_apenas_numeros)))
    # se o cpf nao tem 11 numeros eh invalido
    if len(cpf_apenas_numeros) != 11:
        return  {"validacao":"O seu cpf não possui 11 números. É inválido!"}
    # numeros de dois a dez de formar decrescente
    dois_a_10 = -np.sort(-np.arange(2, 11, 1))
    # de dois a onze de forma desc
    onze_a_2 = -np.sort(-np.arange(2, 12, 1))
    # primeira validacao com o primeiro digito verificador
    primeiro_verificador = sum(dois_a_10 * cpf_apenas_numeros[0:9] * 10) % 11
    # segunda validazao com o segundo digito verificador
    segundo_verificador = sum(onze_a_2 * cpf_apenas_numeros[0:10] * 10) % 11
    if primeiro_verificador == cpf_apenas_numeros[9] and segundo_verificador == cpf_apenas_numeros[10]:
        cpf_result =''.join(str(i) for i in cpf_apenas_numeros)
        return {"mensagem": f'{cpf_result} é valido!'}
        
    else:
        cpf_result =''.join(str(i) for i in cpf_apenas_numeros)
        return {"mensagem": f'{cpf_result} é invalido!'}
