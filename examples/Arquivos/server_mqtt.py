import paho.mqtt.client as mqtt
import time
import datetime
import json
import os

#os.system('mosquitto_sub -h localhost -t test')

def save_image(file):
    try:
        f = open('/home/administrador/face_recognition/examples/FotoRecebida/foto00.jpg', 'wb')
        f.write(bytearray(file))
        f.close()
    except Exception as erro:
        print(erro)

def on_message_server(client, userdata, message):
    #print ("Message received: "  + message.payload)
    print(message.payload)
    # Verifica se é ou não o token
    if(len(message.payload)>=0 and len(message.payload)<=20):
        token= message.payload #String que vem do arduino
        token_test = True
    else:
        token_test = False

    if (not token_test):
        save_image(message.payload)

        # Rodar validação
        # Atualizar registro se o acesso foi ou não valido
        # Publicar se é ou não pra abrir a porta

    if (token_test):
        print('TOKEN Recebido')
        token = str(token)
        #Arrumando o token recebido
        separa_token = (token.split('b'))
        token = separa_token[1]
        separa_token = (token.split("'"))
        token = separa_token[1]
        #
        # def_log = pd.read_csv('/home/victor/Documentos/iot-trab/registros/log.csv')
        registro = {'hora': datetime.datetime.now().timestamp(), 'token': token, 'valido': None, 'imagem': None}
        print(str(os.path.isfile('/home/administrador/face_recognition/examples/FotoRecebida/token.json')))
        # df_log = df_log.append(registro)

        try:
            with open('/home/administrador/face_recognition/examples/FotoRecebida/token.json', 'w') as f:
                json.dump(registro,f)
        except Exception as erro:
            print(erro)

        # client.publish('test',1,1) # Enviando 1 para avisar o raspberry para tirar a foto
        # time.sleep(10) # Esperando o recebimento da foto
clientFoto = mqtt.client()
client = mqtt.Client()
client.on_message=on_message_server
clientFoto.on_message=on_message_server
client.connect('localhost',1883,60)
clientFoto.connect('localhost', 1883, 60)

client.subscribe('test', 1)
clientFoto.subscribe('foto', 1)
clientFoto.loop_forever()
client.loop_forever()
