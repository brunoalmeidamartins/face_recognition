import face_recognition
import json
import os
#Obtendo Imagens do Banco de BancoDadosFotos
path_caminho_banco_fotos = 'BancoDadosFotos/'
path_caminho_banco_token = 'BancoDadosToken/tokens.json'
nome_pessoa = ''
token_recebido = '12345'

try:
    arquivo_json = open(path_caminho_banco_token,'r')
    lista_usuarios = json.load(arquivo_json)
except Exception as erro:
    print("Ocorreu na leitura do arquivo")
    print("O erro eh: {}".format(erro))

#Verificando se o token recebido esta no banco Dados
usuario = lista_usuarios['Usuarios']
banco_contem_token = False
nome_usuario = ''
for i in usuario:
    if i['token'] == str(token_recebido):
        nome_usuario = i['nome']
        banco_contem_token = True
        break;
#Verificando a foto do usuario depois que ela for tirada
face_usuario_encontrada = False
if banco_contem_token == True:
    nome_pasta_usuario = 'BancoDadosFotos/'+nome_usuario+'/'
    lista_arquivos = os.listdir(nome_pasta_usuario)
    for i in lista_arquivos: #Pega todos os nomes dos arquivos da pasta
        path_foto_banco = nome_pasta_usuario+i #Caminho da foto no Banco
        path_foto_recebida = 'FotoRecebida/foto_recebida.jpg' #Caminho da foto recebida

        known_image = face_recognition.load_image_file(path_foto_banco) #Obtem foto que vira do Banco de Dados
        unknown_image = face_recognition.load_image_file(path_foto_recebida) # Imagem que vira da Web Cam

        #Comparacao das Imagens
        biden_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]


        #Resultado da comparacao
        results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
        #Verifico se a imagem recebida "bate" com alguma foto do Banco de BancoDadosFotos
        if str(results) == '[True]':
            print(path_foto_banco)
            face_usuario_encontrada = True
            break
    print("Token esta no banco e seu usuario eh: "+nome_usuario)
else:
    print("Token nao esta no banco!! Acesso Negado")

#Envia comando para abrir porta se toke e face estao contidos no Banco

if face_usuario_encontrada == True:
    print("Envia comando para abrir a porta!!")
else:
    print("Falha na autenticação!!!")
    print("Envia comando para não abrir a porta")





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
