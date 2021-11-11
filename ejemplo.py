from flask import Flask, render_template,request
import os
import random

app=Flask(__name__)

@app.route('/')  #Cuando el usuario entre a esta ruta, ejecuta esta función
def inicio():
    return render_template('login.html')

@app.route('/datos')
def datos():
    user={'nombre':'Juliana'}
    return render_template('datos.html',title='Título Personalizado',user=user)

@app.route('/validar',methods=["POST"])
def validar():
    if request.method=="POST":
        usuario = request.form['usuario']
        password = request.form['password']

        resultado=verificar(usuario,password)
        #return render_template('menu.html',title='Sistema DABM')
        return resultado

@app.route('/monitor')
def monitor():
    #consutar archivo parametros
    datos=getDatos()
    #Obtener lectura
    lectura=random.randint(0,45)
    #Enviar a la interfaz
    color=0
    if lectura >= int(datos[0][1]) and lectura<=int(datos[0][2]):
        color=1
    if lectura >= int(datos[1][1]) and lectura<=int(datos[1][2]):
        color=2
    if lectura >= int(datos[2][1]) and lectura<=int(datos[2][2]):
        color=3
    return render_template('monitor.html',datos=datos, lectura=lectura, color=color)

@app.route('/config')
def config():
    return render_template('config.html')

@app.route('/guardar',methods=["POST"])
def guardar():
    if request.method=="POST":
        minH = request.form['minH']
        maxH = request.form['maxH']
        minN = request.form['minN']
        maxN = request.form['maxN']
        minF = request.form['minF']
        maxF = request.form['maxF']

        directorio=os.path.dirname(__file__)
        nombreArchivo="bd/parametros.csv"
        ruta=os.path.join(directorio,nombreArchivo)
        f=open(ruta,"w")
        datos="Hipotermia"+";"+str(minH)+";"+str(maxH)+"\n"+"Normal"+";"+str(minN)+";"+str(maxN)+"\n"+"Fiebre"+";"+str(minF)+";"+str(maxF)+"\n"
        f.write(datos)
        return render_template('menu.html')

def getDatos():
    directorio=os.path.dirname(__file__)
    nombreArchivo="bd/parametros.csv"
    ruta=os.path.join(directorio,nombreArchivo)
    f=open(ruta,"r")
    lineas=f.readlines()
    f.close()
    datos=[]
    for l in lineas:
        l=l.replace("\n","")
        l=l.split(";")
        datos.append(l)
    return datos

def verificar(usuario,password):
    fileUsers="C:\\Users\\julia\\OneDrive - ESCUELA COLOMBIANA DE INGENIERIA JULIO GARAVITO\\Documents\\CódigosDABM\\Flask\\bd\\users.csv"
    f=open(fileUsers,"r")
    datos=f.readlines()
    f.close()
    usuarios=[]
    for d in datos:
        d=d.replace("\n","")
        d=d.split(";")
        usuarios.append(d)
        for i in usuarios:
            #usuarioR=usuarios[i][0]
            #passwordR=usuarios[i][1]
            if usuario==i[0]:
                if password==i[1]:
                    res=True
                    #return render_template('interfaz.html')
                else:
                    res='contraseña'
                    #return "Contraseña incorrecta"
            else:
                res='usuario'
                #return "usuario no encontrado"
    if res==True:
        return render_template('menu.html')
    elif res=='contraseña':
        return "Contraseña incorrecta"
    elif res=='usuario':
        return "usuario no encontrado"


if __name__=="__main__":
    app.run(debug=True)