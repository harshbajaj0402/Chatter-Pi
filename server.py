import socket,time
import sounddevice as sd
from scipy.io.wavfile import write
from scipy.io import wavfile
from _thread import *
import wave,random,struct,queue,pyaudio,threading,sys,os
import numpy as np
from pydub import AudioSegment
from pydub.playback import play


CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "utput.wav"
WIDTH = 2

clin = None
print_lock = threading.Lock() 

def text(cl,t):
    tex = 'text'    
    cl.send(tex.encode('utf-8')) 
    cl.send(t.encode('utf-8')) 

def audio(c):
    txt = 'start'
    c.send(txt.encode('utf8'))
    
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)
    q = queue.Queue()
    frames = []
    stream.start_stream()
    data = c.recv(CHUNK)
    lenn = len(data)
    while lenn != 0:
        q.put(data)
        if not q.empty():
            print('don')
            stream.write(q.get())
        print('w')
        stream.write(data)
        print('r')
        data = c.recv(CHUNK)
        if data == b'last':
            break
        print('l')
        lenn = len(data)
        print('a')
        frames.append(data)
        print('done appending')
    print('started creating file')
    obj = wave.open('sound.wav','wb')
    obj.setnchannels(1) # mono
    obj.setsampwidth(2)
    obj.setframerate(RATE)
    for i in range(3):
        value = random.randint(-32767, 32767)
        data = struct.pack('<h', value)
        obj.writeframesraw(b''.join(frames) )
        print("done receiving")
    song = AudioSegment.from_wav("sound.wav")
    play(song)

    print('done')     
    
    stream.stop_stream()
    stream.close()
    p.terminate()

def close(c):
    message = 'Good Night...'
    c.send(message.encode('utf-8'))
    print(message)
    c.close() 
    print_lock.release()    
    #rply = input('do want to want to exit:\n')
    #if rply == 'yes':
    #   os._exit(0)                
        
# thread fuction 
def threaded(cl,message,tex=""):
        
        #mes='Audio file requested, press y'
        #c.send(mes.encode('utf8'))
    messag=int(message)    
    if messag == 1:
        text(cl,tex)  
    elif messag == 2:
        audio(cl) 
    elif messag == 3:
        close(cl)            # cection closed   
  
def Main(n): 
    soc = socket.socket()
    host_name = socket.gethostname()
    ip = socket.gethostbyname(host_name)
    port = 12345
    soc.bind((host_name, port))
    print(host_name, '({})'.format(ip))
    name = n
    soc.listen(1) #Try to locate using socket
    print('Waiting for incoming connections...')
    # a forever loop until client wants to exit 
     
    # establish connection with client 
    c, addr = soc.accept() 

    # lock acquired by client 
    print_lock.acquire() 
    print('Connected to :', addr[0], ':', addr[1]) 
    
    # Start a new thread and return its identifier  
    # clin = c
    # ret(clin)
    return c
    soc.close() 
  
  

