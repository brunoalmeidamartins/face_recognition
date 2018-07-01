from Adafruit_IO import *
import time

#aio = Client('Bruno_Martins')
aio = Client('fcc627a3b049457594b3e44b8f7333f6')
#ADAFRUIT_IO_USERNAME = 'fcc627a3b049457594b3e44b8f7333f6'


while True:
    data = aio.receive('Botao_Porta')
    if data.value == 'Aberta':
        #print('Dados recebidos: {0}'.format(data.value))
        print('Porta Aberta!!')
        aio.send('test','Porta Aberta')
        time.sleep(3)
        aio.send('Botao_Porta','Fechada')
        aio.send('test','Porta Fechada')
        print('Porta Fechada!!!')
    time.sleep(1)
