import face_recognition
import json
import os
import time
import paho.mqtt.client as mqtt
from datetime import datetime

from Adafruit_IO import * ##Enviar os dados para Adafruit
aio = Client('fcc627a3b049457594b3e44b8f7333f6') # Client Adafruit

#Obtendo Imagens do Banco de BancoDadosFotos
path_caminho_banco_fotos = '/home/administrador/face_recognition/examples/BancoDadosFotos/'
path_caminho_banco_token = '/home/administrador/face_recognition/examples/BancoDadosToken/tokens.json'
nome_pessoa = ''
token_recebido = ''

# Conexao com broker
client = mqtt.Client()
#client.connect('192.168.43.218',1883,60)
client.connect('localhost',1883,60) #Retirar isso daqui na hora
def envia_msg_broker(msg): ##Funcao de Publicacao no broker
    client.publish('test',msg)

def envia_msg_adafruit(msg): ##Envia msg online
    if msg == 'Aberta':
        aio.send('Botao_Porta',msg)
        aio.send('test','Porta '+msg)
    else:
        aio.send('Botao_Porta',msg)
        aio.send('test','Porta '+msg)

def envia_msg_log_adafruit(msg): ## Envia log para adafruit online
    now = datetime.now()
    string = (str(now.day) +'/'+str(now.month)+'/'+str(now.year)+' '+str(now.hour)+':'+str(now.minute)+':'+str(now.second))
    aio.send('Log',msg + string )




#Limpando a pasta
def limpa_pasta_arquivos():
    if len(os.listdir('/home/administrador/face_recognition/examples/FotoRecebida/')) > 0:
        lista_arquivos = os.listdir('/home/administrador/face_recognition/examples/FotoRecebida/')
        for i in lista_arquivos:
            os.remove('/home/administrador/face_recognition/examples/FotoRecebida/'+str(i))

limpa_pasta_arquivos()
#token_recebido = '12345'

num = 0 # trocar depois e apagar
os.system('clear')
print('Inicie o Processo')
while (num == 0): # trocar por true
    time.sleep(2)

    ##Abrindo a porta externamente
    data = aio.receive('Botao_Porta')
    if data.value == 'Aberta':
        print('Porta Aberta Externamente!!')
        aio.send('test','Porta Aberta')
        envia_msg_broker('a') # Envia comando para abrir a porta para o broker
        time.sleep(3)
        aio.send('Botao_Porta','Fechada')
        aio.send('test','Porta Fechada')
        envia_msg_log_adafruit('Porta Aberta Externamente! ')
        time.sleep(2)
        os.system('clear')
        print("Inicie o processo novamente")
        limpa_pasta_arquivos()
        pass
    ## Fim abertura de porta externamente

    if len(os.listdir('/home/administrador/face_recognition/examples/FotoRecebida/')) == 1 and num != 1:
        token_nao_cadastrado = False
        print("Token recebido!! Analisando ...")
        try:
            arquivo_json = open('/home/administrador/face_recognition/examples/FotoRecebida/token.json', 'r')
            token = json.load(arquivo_json)
            token_recebido = token['token']
        except Exception as erro:
            print("Ocorreu na leitura do arquivo")
            print("O erro eh: {}".format(erro))
            limpa_pasta_arquivos()
        try:
            arquivo_json = open(path_caminho_banco_token,'r')
            lista_usuarios = json.load(arquivo_json)
        except Exception as erro:
            print("Ocorreu na leitura do arquivo")
            print("O erro eh: {}".format(erro))
            #Apaga o arquivo para que a leitura seja feita novamente
            limpa_pasta_arquivos()
        #Verificando se o token recebido esta no banco Dados
        usuario = lista_usuarios['Usuarios']
        banco_contem_token = False
        nome_usuario = ''
        for i in usuario:
            if i['token'] == str(token_recebido):
                nome_usuario = i['nome']
                banco_contem_token = True
                break
        if(banco_contem_token):
            print("Token Encontrado!!")
            #print(nome_usuario)
            #limpa_pasta_arquivos()
        else:
            print("Nao esta no banco")
            limpa_pasta_arquivos()

            envia_msg_broker('e')
            envia_msg_log_adafruit('Tentativa de acesso: ' + token_recebido + ' ')

            token_nao_cadastrado = True
            pass
        if (not token_nao_cadastrado):
            print("Aguardando a autenticacao por foto ...")
            #client = mqtt.Client()
            #client.connect('192.168.43.218',1883,60)
            #client.publish('test','c')
            envia_msg_broker('f') #Envia msg para tirar foto
            time.sleep(10)
            print("Acabou o tempo!! Analisando se a foto chegou ...")
            #Aguarda ate a foto chegar
        if (len(os.listdir('/home/administrador/face_recognition/examples/FotoRecebida/')) == 2):
            #Verificando a foto do usuario depois que ela for tirada
            face_usuario_encontrada = False
            if banco_contem_token == True:
                nome_pasta_usuario = '/home/administrador/face_recognition/examples/BancoDadosFotos/'+nome_usuario+'/'
                lista_arquivos = os.listdir(nome_pasta_usuario)
                print("Foto ok!!! Analisando a foto no banco de dados ...")
                for i in lista_arquivos: #Pega todos os nomes dos arquivos da pasta
                    path_foto_banco = nome_pasta_usuario+i #Caminho da foto no Banco
                    path_foto_recebida = '/home/administrador/face_recognition/examples/FotoRecebida/foto00.jpg' #Caminho da foto recebida

                    known_image = face_recognition.load_image_file(path_foto_banco) #Obtem foto que vira do Banco de Dados
                    unknown_image = face_recognition.load_image_file(path_foto_recebida) # Imagem que vira da Web Cam

                    #Comparacao das Imagens
                    biden_encoding = face_recognition.face_encodings(known_image)[0]
                    try:
                        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
                    except Exception as e:
                        limpa_pasta_arquivos()
                        break


                    #Resultado da comparacao
                    results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
                    #Verifico se a imagem recebida "bate" com alguma foto do Banco de BancoDadosFotos
                    if str(results) == '[True]':
                        #print(path_foto_banco)
                        face_usuario_encontrada = True
                        break
            else:
                print("Token nao esta no banco!! Acesso Negado")
                limpa_pasta_arquivos()

                envia_msg_broker('e') #Envia comando de erro para broker

                envia_msg_log_adafruit('Token nao esta no banco! ')

                continue




            #Envia comando para abrir porta se toke e face estao contidos no Banco
            print("Analisando Foto!! Enviando resposta ...")
            time.sleep(2)
            if banco_contem_token == True and face_usuario_encontrada == True:
                print('Seja Bem vindo:'+nome_usuario)
                print("Envia comando para abrir a porta!!")

                envia_msg_broker('a') # Envia comando para abrir a porta para o broker
                envia_msg_adafruit('Aberta') #Envia msg para Adafruit porta aberta
                time.sleep(5)

                envia_msg_adafruit('Fechada')
                time.sleep(1)
                envia_msg_log_adafruit('Acesso Concedido: '+nome_usuario+ ' ')

                os.system('clear')
                print("Inicie o processo novamente")

            else:
                print("Falha na autenticação!!!")
                print("Envia comando para não abrir a porta")

                envia_msg_broker('e') #Envia comando de erro para o broker
                envia_msg_log_adafruit('Tentativa de acesso: ' + token_recebido + ' ')

                time.sleep(5)
                os.system('clear')
                print("Inicie o processo novamente")
                print(" ")
            limpa_pasta_arquivos()
        else:
            print("Tempo de espera acabou e a foto nao foi tirada")
            print("Reinicie o processo")

            envia_msg_broker('e') #Envia comando de erro para broker
            envia_msg_log_adafruit('Tentativa de acesso: ' + token_recebido + ' ')

            print(" ")
            time.sleep(3)
            os.system('clear')
            print("Inicie o processo novamente")
            limpa_pasta_arquivos()
    else:
        #Apaga todos os arquivos e reinicia o processo
        if len(os.listdir('/home/administrador/face_recognition/examples/FotoRecebida/')) > 0:
            limpa_pasta_arquivos()
            print('Comece o processo novamente')

            envia_msg_broker('e') #Envia comando de erro para broker

        continue
