import socket 
import time  
import pyaudio
CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

stream.start_stream()

def Main(): 
    soc = socket.socket()
    shost = socket.gethostname()
    ip = socket.gethostbyname(shost)
    #get information to connect with the server
    print(shost, '({})'.format(ip))
    #server_host = input('Enter server\'s IP address:')
    server_host = '192.168.2.19'
    name = input('Enter Client\'s name: ')
    port = 2233
    print('Trying to connect to the server: {}, ({})'.format(server_host, port))
    time.sleep(1)
    soc.connect((server_host, port))
    print("Connected...\n")
    
    while True:
        mes=soc.recv(4096)
        print("mes:",mes.decode('utf-8'))
        #mesg=soc.recv(4096)
        if mes.decode('utf-8') == 'start': 
            print("*_>recording")
            
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                try:
                    data = stream.read(CHUNK,exception_on_overflow = False)
                except Exception as e:
                    print (e)
                    data='\x00' * CHUNK

                print (len(data))
                soc.sendall(data)

            print("*_>done recording")

            stream.stop_stream()
            stream.close()
            p.terminate()

            print("*_>closed") 
            d=b'last'    
            soc.send(d)
        elif mes.decode('utf-8') == 'text':
            tx = soc.recv(4096)
            print(tx.decode('utf-8'))
        elif mes.decode('utf-8') == 'Good Night...':
            soc.close()    # close the connection 
            print("closing")
            break         
    
     
  
if __name__ == '__main__': 
    Main() 
