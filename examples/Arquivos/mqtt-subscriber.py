import paho.mqtt.client as mqtt
import time
import json

def on_message(client, userdata, message):
    print ("Message received: "  + str(message.payload))
    # print((message.payload[0]))

with open('/home/administrador/face_recognition/examples/BancoDadosFotos/Bruno/bruno3.jpg', 'rb') as imageFile:
#with open('/home/administrador/face_recognition/examples/BancoDadosFotos/Victor/biden.jpg', 'rb') as imageFile:
    f = imageFile.read()
    # b = bytearray(f)

client = mqtt.Client()
client.on_message=on_message

client.connect('localhost',1883,60)

client.loop_start()
#for i in range(100):
try:
    client.publish('test',f,1)
    #client.publish('test',json.dumps({'token':'9371937povdad'}))
    # client.publish('test','onfnnfa',1)
except KeyboardInterrupt:
    pass

# time.sleep(4)

# client.subscribe('test', 1)
# f = open('/home/victor/Imagens/perfilPayload.jpg', 'wb')
# f.write(bytearray(payload))
# f.close()

client.loop_stop()
client.disconnect()
