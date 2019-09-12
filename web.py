from flask import Flask
from flask import render_template,Response,url_for,redirect,request
import server as s
import client as c
import sys
import time
from flask import jsonify
from multiprocessing import Process, Value

app = Flask(__name__)


@app.route('/')
def home():
   return render_template('index.html')

@app.route('/from')   
def server():
   return render_template('selection.html')

@app.route('/selection')
def select():
   global cl
   cl=s.Main(sys.argv[1])
   print(cl)
   return redirect(url_for('server'))

@app.route('/audio')
def audiomsg():
   s.threaded(cl,2)
   return redirect(url_for('server'))

@app.route('/close')
def closec():
   s.threaded(cl,3)
   return redirect(url_for('home'))

@app.route('/text',methods=["GET","POST"])
def tesxtmsg():
   if request.method=='POST':
      text = request.form.get('text1')
      print(text)
      s.threaded(cl,1,text)
      return redirect(url_for('server'))
   
if __name__ == '__main__':
   
   app.run(debug=True, use_reloader=False)
   cl=s.Main(sys.argv[1])
   
