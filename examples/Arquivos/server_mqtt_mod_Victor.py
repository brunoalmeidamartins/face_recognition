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

        #g = open('/home/administrador/face_recognition/examples/BancoDadosFotos/Gabriel/foto00.jpg', 'wb')
        #g.write(bytearray(file))
        #g.close()
    except Exception as erro:
        print(erro)

def on_message_server(client, userdata, message):
    #print ("Message received: "  + message.payload)
    print(message.payload)
    # Verifica se é ou não o token
    caracter = False
    if(len(message.payload)>=0 and len(message.payload)<=20):
        token= message.payload #String que vem do arduino
        if(len(token) < 5):
            caracter = True
            print('Nao eh token')
            return
        token_test = True

    else:
        token_test = False

    if (not token_test):
        save_image(message.payload)

        # Rodar validação
        # Atualizar registro se o acesso foi ou não valido
        # Publicar se é ou não pra abrir a porta

    # Caracter foi recebido
    if (not token_test and caracter):
        key = token
        separa_key = (key.split('b'))
        key = separa_key[1]
        separa_key = (key.split("'"))
        key = separa_key[1]

        # Se for o caracter para tirar a foto não se faz nada
        if (key == 'f'):
            pass
        # Se for um caracter de erro ou aprovação será armazenado um log
        else:
            number = len(os.listdir('/home/administrador/face_recognition/examples/BancoDadosFotos/FotoLog/'))

            foto_test = True
            try:
                os.rename('/home/administrador/face_recognition/examples/FotoRecebida/foto00.jpg',
                        '/home/administrador/face_recognition/examplesBancoDadosFotos/FotoLog/foto'+str(number)+'.jpg')
            except Exception as erro:
                foto_test = False
                print(e)
                print(Foto nao retirada)

            last_log = json.loads(open('/home/administrador/face_recognition/examples/FotoRecebida/token.json').read())

            # Verificando se a porta foi ou não aberta
            if (key == 'e'):
                valido = False
            if (key == 'a'):
                valido = True

            last_log['valido'] = valido

            # Se foi salva uma foto ele prepara o log com o seu caminho no banco de fotos
            if (foto_test)
                last_log[imagem] = '/home/administrador/face_recognition/examplesBancoDadosFotos/FotoLog/foto'+str(number)+'.jpg'
            else:
                last_log[imagem] = 'NaN'

            # Abrindo logs anteriores e salvando o novo
            try: # Evita error se os logs ainda não existirem
                with open('/home/administrador/face_recognition/examples/Logs/log.json') as f:
                    logs = json.load(f)

                logs.update(last_log)
            except:
                logs = last_log

            with open('/home/administrador/face_recognition/examples/Logs/log.json', 'w') as f:
                json.dump(logs, f)


    # Token foi recebido
    if (token_test and not caracter):
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
#clientFoto = mqtt.client()
client = mqtt.Client()
client.on_message=on_message_server
#clientFoto.on_message=on_message_server
client.connect('localhost',1883,60)
#clientFoto.connect('localhost', 1883, 60)

client.subscribe('test', 1)
#clientFoto.subscribe('foto', 1)
#clientFoto.loop_forever()
client.loop_forever()
