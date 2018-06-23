import face_recognition
import json
import os
import time
#Obtendo Imagens do Banco de BancoDadosFotos
path_caminho_banco_fotos = '/home/administrador/face_recognition/examples/BancoDadosFotos/'
path_caminho_banco_token = '/home/administrador/face_recognition/examples/BancoDadosToken/tokens.json'
nome_pessoa = ''
token_recebido = ''

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
    if len(os.listdir('/home/administrador/face_recognition/examples/FotoRecebida/')) == 1 and num != 1:
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
            break
        print("Aguardando a autenticacao por foto ...")
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
                    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]


                    #Resultado da comparacao
                    results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
                    #Verifico se a imagem recebida "bate" com alguma foto do Banco de BancoDadosFotos
                    if str(results) == '[True]':
                        #print(path_foto_banco)
                        face_usuario_encontrada = True
                        break
            else:
                print("Token nao esta no banco!! Acesso Negado")


            #Envia comando para abrir porta se toke e face estao contidos no Banco
            print("Foto analisando!! Enviando resposta ...")
            time.sleep(2)
            if banco_contem_token == True and face_usuario_encontrada == True:
                print('Seja Bem vindo:'+nome_usuario)
                print("Envia comando para abrir a porta!!")
                time.sleep(5)
                os.system('clear')
                print("Inicie o processo novamente")

            else:
                print("Falha na autenticação!!!")
                print("Envia comando para não abrir a porta")
                time.sleep(5)
                os.system('clear')
                print("Inicie o processo novamente")
                print(" ")
            limpa_pasta_arquivos()
        else:
            print("Tempo de espera acabou e a foto nao foi tirada")
            print("Reinicie o processo")
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
        continue

"""
known_image = face_recognition.load_image_file("BancoDadosFotos/Bruno/Rosto/bruno1.jpg") #Obtem que vira do Banco de Dados
unknown_image = face_recognition.load_image_file("BancoDadosFotos/Bruno/obama.jpg") # Imagem que vira da Web Cam


#Comparacao das Imagens
biden_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]


#Resultado da comparacao
results = face_recognition.compare_faces([biden_encoding], unknown_encoding)

print(results)
"""
