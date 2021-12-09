import socket,cv2, pickle,struct,imutils
from cryptography.fernet import Fernet
import rsa

#vygeneruje klíč a uloží jej do souboru
key = Fernet.generate_key()#vygenerovat 256bitový klíč
fernet = Fernet(key) #vytvořit instanci s klíčem jako argumentem konstruktoru
with open('Key.key','wb') as f:
    f.write(key) #zápis klíče do souboru .key



# Socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#host_name  = socket.gethostname()
host_name = "127.0.0.1"
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 9999
socket_address = (host_ip,port)

# Socket
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:",socket_address)



# Socket Accept
while True:
	client_socket,addr = server_socket.accept()
	print('GOT CONNECTION FROM:',addr)
	f = open("pub_client_key.pem", "wb")
	data = client_socket.recv(1024)
	f.write(data)
	f = open("pub_client_key.pem", "rb")
	pubKey = rsa.PublicKey.load_pkcs1(f.read())
	message = open('key.key', "rb")
	text = message.read()
	data = rsa.encrypt(text, pubKey)
	client_socket.sendall(data)



	if client_socket:
		vid = cv2.VideoCapture(0)
		
		while(vid.isOpened()):
			img,frame = vid.read()
			frame = imutils.resize(frame,width=500)
			a = pickle.dumps(frame) #převést obrazová data na hexadecimální
			a=fernet.encrypt(a) #zašifrovat hexadecimální text
			message = struct.pack("Q",len(a))+a #balení dat do balíků
			client_socket.sendall(message)#odesílání šifrovaných dat klientovi

			cv2.imshow('TRANSMITTING VIDEO',frame)
			key = cv2.waitKey(1) & 0xFF
			if key ==ord('q'):
				client_socket.close()
