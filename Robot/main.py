#######################################################Conexión con arduino provisional
from pydoc import resolve
from time import process_time_ns, time
from idna import alabel
import serial
ser   = serial.Serial(port = '/dev/ttyACM0',
                         baudrate = 9600,
                         bytesize = serial.EIGHTBITS,
                         parity   = serial.PARITY_NONE,
                         stopbits = serial.STOPBITS_ONE)

#######################################################BUSQUEDA DE INTERNET
#Importamos las libresias necesarias
import requests #Peticiones
from googlesearch import search#Google searcher
from bs4 import BeautifulSoup #BeautifulSoup version 4

REPOSITORIO='programarya'
#Funcion searcher en google:
def getGoogleSearch(query):
    #configuramos los parámetros de la busqueda:
    print(query)
    tld = 'com'
    lang = 'es'
    num = 2
    start = 0
    stop = num
    pause = 3.0
    #Obtenemos los resultados de la búsqueda:
    try:
        results = search(query,num_results=num,lang=lang)
        #results = search(query,lang=lang,num=num,start=start,stop=stop,pause=pause)
        genArray = ['Google Results ->']
        for res in results:
            genArray.append(res)
        return genArray
    except Exception as e:
        array = []
        array.append("Error en el servidor: "+str(e))
        return array

#Funcion de webscrapping en web seleccionada
def getWebResults(urls, keyword,n): #url: Objetivo de Scrapper, keyword: elemento en DOM a buscar
    try:
        url=urls[n]
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        genArray = []
        SoupObject = soup.find_all(keyword)#Se le pasa el objetivo del DOM a buscar
        for res in SoupObject:
            genArray.append(res.get_text())
        if len(genArray)==0:
            SoupObject = soup.find_all('pre')#Se le pasa el objetivo del DOM a buscar
            for res in SoupObject:
                genArray.append(res.get_text())
        if(len(genArray)>0):
            aux="/*       Resumen General        */\n"
            i=0
            posibles=""
            auxArray=[]
            while i<len(genArray):
                res=genArray[i]
                if '\n' in res:
                   aux=aux+res+"\n"
                   auxArray.append(res)
                   aux=aux+"/*        ...          */\n"
                else:
                    j=i
                    while '\n' in res or j<len(genArray):
                        res=genArray[j]
                        posibles=posibles+res+"\n"
                        j+=1
                    if j!=i:
                        i=j-1
                i+=1
            genArray=[]
            if posibles!="":
                aux=aux+"/*       Posibles resultados correctos       */\n"+posibles
            for res in auxArray:
                genArray.append(res)
            genArray.append(aux)
            if posibles!="":
                genArray.append("/*        Posibles datos utiles        */\n"+posibles)
    except:
        if n<len(urls):
            genArray=getWebResults(urls,keyword,n+1)
        else:
            genArray=[]
            genArray.append('Sin resultados')
    return genArray

def ObtenerRepositoriosD():
    with open('DICCIONARIOS/RepositoriosDefinicion.txt') as archivo:
        i=0
        rep=[]
        for linea in archivo:
            rep.append(linea.replace("\n",""))
    return rep
def buscaWebDef(Con,Val):
        REPOSITORIODEF=ObtenerRepositoriosD()
        codeArray=None
        googleArray=None
        i=0
        Con=Con
        Com=False
        while Com!=True:
            aux=[]
            busqueda=Val+":"+REPOSITORIODEF[i]
            googleArray = getGoogleSearch(str(busqueda))  #sintaxis+while+java:programarya
            print(googleArray)
            codeArray = getWebResults(googleArray, 'p',0)
            i+=1
            if (len(codeArray)>1):
                aux=[]
                aux.append(codeArray[0])
                aux.append(codeArray[len(codeArray)-1])
                codeArray=aux
            if len(codeArray)>1 or i>=len(REPOSITORIODEF):
                Com=True
        if (len(codeArray)>0):
            return True, codeArray
        else:
            return False,[]
#######################################################SINTESIS Y RECONOCIMIENTO DE VOZ
import speech_recognition as sr
#import pyttsx3
import multiprocessing as pr
mic_name = "default"
sample_rate = 48000
chunk_size = 2048
ID_MIC=0
r = sr.Recognizer()
sr.dynamic_energy_threshold = False
r.dynamic_energy_threshold = False
mic_list = sr.Microphone.list_microphone_names()
for i, microphone_name in enumerate(mic_list):
    if microphone_name == mic_name:
        ID_MIC = i  
def asistenteRespuesta(texto):
    """
    import pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print("------------------------")
        print(" - ID: %s"        % voice.id)
        print(" - Nombre: %s"    % voice.name)
        print(" - Lenguajes: %s" % voice.languages)
        print(" - Genero: %s"    % voice.gender)
        print(" - Edad: %s"      % voice.age)
    engine.setProperty("rate", 140) # Control de velocidad
    engine.setProperty("voice","spanish-latin-am")
    text = " "+texto
    engine.say(" ")
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    """""
    import espeakng
    mySpeaker = espeakng.Speaker()
    mySpeaker.pitch = 80
    mySpeaker.wpm = 120
    mySpeaker.voice = 'es'
    mySpeaker.say(texto,wait4prev=True)

def reconocer():
    with sr.Microphone(device_index = ID_MIC, sample_rate = sample_rate, 
                        chunk_size = chunk_size) as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text=r.recognize_google(audio,language="es-mx")
            mensaje='{}'.format(text)
            return mensaje
        except sr.UnknownValueError:
            print("----")
        except sr.RequestError as e:
            asistenteRespuesta("Lo siento, puede que no tengas conexión a internet.")

####################################################### MODULOS DE IDENTIFICACIÓN
from difflib import SequenceMatcher as SM

def Coincidencia(text1,text2):
    return (SM(None, text1, text2).ratio())
def CompararDict(mensaje, diccionario):
    ENCONTRADO=False
    for linea in diccionario:
        LINEAN = linea.replace('\n','')
        concidencia=Coincidencia(mensaje,LINEAN)
        if(concidencia>0.90):
            print("coincidencia: "+str(concidencia))
            ENCONTRADO=True
            break
    return ENCONTRADO
def CompararDictCom(mensaje, diccionario):
    ENCONTRADO=False
    for linea in diccionario:
        LINEAN = linea.replace('\n','')
        aux1=LINEAN.split(" ")
        aux2=mensaje.split(" ")
        if len(aux2)>len(aux1):
            concidencia=0
            val=0
            for pal in aux1:
                concidencia+=Coincidencia(pal, aux2[val]) / len(aux1)
                val+=1
            if(concidencia>0.90):
                mensaje=''
                print("coincidencia: "+str(concidencia))
                while val < len(aux2):
                    mensaje+=aux2[val]+" "
                    val+=1
                print("----"+mensaje)
                ENCONTRADO=True
                return ENCONTRADO, mensaje
        return ENCONTRADO, mensaje

def BuscarEnDict(mensaje):
    PALABRA=''
    if CompararDict(mensaje,open("DICCIONARIOS/1PARAR.txt","r"))==True:
        return 'PARAR', mensaje
    elif CompararDict(mensaje,open("DICCIONARIOS/1DELANTE.txt","r"))==True:
        return 'DELANTE', mensaje
    elif CompararDict(mensaje,open("DICCIONARIOS/1DETRAS.txt","r"))==True:
        return 'ATRAS', mensaje
    elif CompararDict(mensaje,open("DICCIONARIOS/1DERECHA.txt","r"))==True:
        return 'DERECHA', mensaje
    elif CompararDict(mensaje,open("DICCIONARIOS/1IZQUIERDA.txt","r"))==True:
        return 'IZQUIERDA', mensaje
    elif CompararDict(mensaje,open("DICCIONARIOS/1GDERECHA.txt","r"))==True:
        return 'GDERECHA', mensaje
    elif CompararDict(mensaje,open("DICCIONARIOS/1GIZQUIERDA.txt","r"))==True:
        return 'GIZQUIERDA', mensaje
    elif CompararDict(mensaje,open("DICCIONARIOS/1GDERECHAT.txt","r"))==True:
        return 'GDERECHAT', mensaje
    elif CompararDict(mensaje,open("DICCIONARIOS/1GIZQUIERDAT.txt","r"))==True:
        return 'GIZQUIERDAT', mensaje
    elif CompararDict(mensaje,open("DICCIONARIOS/1LUZ.txt","r"))==True:
        return 'ELUZ', mensaje
    elif CompararDict(mensaje,open("DICCIONARIOS/1LUZAP.txt","r"))==True:
        return 'ALUZ', mensaje 
    elif CompararDict(mensaje,open("DICCIONARIOS/1DONDE.txt","r"))==True:
        return 'DONDE', mensaje 
    else:
        web,men= CompararDictCom(mensaje,open("DICCIONARIOS/2BUSQUEDA.txt","r"))
        if web==True:
            asistenteRespuesta('Por su puesto, dame un momento')
            return 'WEB', men
        return 'NULL', mensaje

def identificar(mensaje):
    try:
        mensaje = mensaje.upper()
    except:
        return False,'NONE','Disculpa, no te escuche.'
    longitud = len(mensaje)
    if(longitud<2):
        return False,'NO', ''
    print(mensaje)
    Tipo, mensaje2=BuscarEnDict(mensaje)
    print(Tipo)
    if (Tipo == 'DELANTE'):
        asistenteRespuesta("ENTENDIDO,   AVANZANDO!!!")
        ser.write(b'a')
        return True,Tipo,mensaje2
    elif (Tipo == 'ATRAS'):
        asistenteRespuesta("   RETROCEDIENDO!!!")
        ser.write(b'O')
        return True,Tipo,mensaje2
    elif (Tipo == 'DERECHA'):
        asistenteRespuesta("   DERECHA!!!")
        ser.write(b'r')
        return True,Tipo,mensaje2
    elif (Tipo == 'IZQUIERDA'):
        asistenteRespuesta("   IZQUIERDA!!!")
        ser.write(b'l')
        return True,Tipo,mensaje2
    elif (Tipo == 'GDERECHA'):
        asistenteRespuesta("   GIRANDO A LA IZQUIERDA!!!")
        ser.write(b'L')
        return True,Tipo,mensaje2
    elif (Tipo == 'GIZQUIERDA'):
        asistenteRespuesta("   GIRANDO A LA DERECHA!!!")
        ser.write(b'R')
        return True,Tipo,mensaje2
    elif (Tipo == 'GDERECHAT'):
        asistenteRespuesta("   GIRANDO A LA DERECHA!!!")
        ser.write(b'X')
        return True,Tipo,mensaje2
    elif (Tipo == 'GIZQUIERDAT'):
        asistenteRespuesta("   GIRANDO A LA IZQUIERDA!!!")
        ser.write(b'Y')
        return True,Tipo,mensaje2
    elif (Tipo == 'PARAR'):
        asistenteRespuesta("   DETENIENDO!!!")
        ser.write(b'D')
        return True,Tipo,mensaje2
    elif (Tipo == 'ELUZ'):
        asistenteRespuesta("   CLARO QUE SI!!!")
        ser.write(b'Z')
        return True,Tipo,mensaje2
    elif (Tipo == 'ALUZ'):
        asistenteRespuesta("   POR SU PUESTO!!")
        ser.write(b'P')
        return True,Tipo,mensaje2
    elif (Tipo == 'DONDE'):
        asistenteRespuesta("   AQUI ESTOY!!")
        ser.write(b'n')
        return True,Tipo,mensaje2
    elif Tipo == 'WEB':
        Con=mensaje2
        Val=mensaje2.replace(" ","+")
        ser.write(b'T')
        ser.write(b'H')
        exito,res=buscaWebDef(Con,Val)
        if exito == True:
            asistenteRespuesta(res[0])
        else:
            asistenteRespuesta("Lo siento, no encontre resultados.")
    else :
        respuesta=conversacion(mensaje)
        if len(respuesta)>0:
            import random
            opcion=random.randint(0,3)
            if opcion==0:
                ser.write(b't')
            elif opcion==1:
                ser.write(b'H')
            elif opcion==2:
                ser.write(b'L')
                ser.write(b'R')
            elif opcion==3:
                ser.write(b'R') 
                ser.write(b'L')
            asistenteRespuesta(respuesta[random.randint(0, len(respuesta)-1)])
            return True,"Conversacion",mensaje2
        else:
            mensaje2=mensaje2.upper()
            if 'EL' in mensaje2:
                m=mensaje2.split("EL")
                print(m[1])
                asistenteRespuesta("¿Que es el "+m[1]+"?")
            else:
                asistenteRespuesta("No comprendi, disculpa")
            return False,"NULL",mensaje2

##################################################### Conversación

def conversacion(texto):
    CEREBRO="DICCIONARIOS/Conversacion.yml"
    linea=0
    Total=LineasTotales(CEREBRO)
    arreglo=[]
    while linea<Total:
        with open(CEREBRO) as f:
            Contenido=f.readlines()[:]
            data = Contenido[linea]
            data = data.replace("\n","")
            data=data.upper()
            if '- - ' in data and probabilidad(data,texto)>70:
                linea+=1
                respuesta=''
                while linea<Total:
                    respuesta = Contenido[linea]
                    respuesta = respuesta.replace("\n","")
                    if '- - ' in respuesta:
                        break
                    else:
                        arreglo.append(respuesta)
                    linea+=1
                break
            linea+=1
    return arreglo


def LineasTotales(ARCHIVO):
    with open(ARCHIVO) as myfile:
        total_lines = sum(1 for line in myfile)
    return total_lines-1
def probabilidad(diccionario,texto):
    diccionario=diccionario.replace('- - ','')
    print(diccionario+"===="+texto)
    probabilidad=0
    for letra in texto:
        if letra in diccionario:
            probabilidad+=1
    print(str(probabilidad)+"   "+str(len(texto)))
    probabilidad=probabilidad*10/len(texto)

    dic = diccionario.split(" ")
    text = texto.split(" ")
    probabilidad3=0
    if len(dic)>len(text):
        for t in text:
            for d in dic:
                if Coincidencia(t,d)>.70:
                    probabilidad3+=1
                    break
    else:
        for d in dic:
            for t in text:
                if Coincidencia(t,d)>.70:
                    probabilidad3+=1
                    break
    probabilidad3=probabilidad3*30/len(text)
    probabilidad2=Coincidencia(diccionario,texto)*60


    print("%"+str(probabilidad))
    print("%"+str(probabilidad2))
    print("%"+str(probabilidad3))
    return probabilidad+probabilidad2+probabilidad3

##################################################################################

import time
def aleatorio():
    while True:
        ser.write(b'k')
        time.sleep(5)

#################################################################################
from email.mime import image
import cv2
Cara_Proto="Deteccion_Cara/opencv_face_detector.pbtxt"
Cara_Modelo="Deteccion_Cara/opencv_face_detector_uint8.pb"
Cara_Net=cv2.dnn.readNet(Cara_Modelo,Cara_Proto)
def resaltar(net, frame, conf_threshold=0.7):
    frameOpencvDnn=frame.copy()
    Alto_Frame=frameOpencvDnn.shape[0]
    Ancho_Frame=frameOpencvDnn.shape[1]
    blob=cv2.dnn.blobFromImage(frameOpencvDnn, 1.2, (300,300), [104, 117, 123], True, False)
    net.setInput(blob)
    Detecciones=net.forward()
    Cara_Rect=[]
    x1=0
    y1=0
    x2=0
    y2=0
    for i in range(Detecciones.shape[2]):
        confidence=Detecciones[0,0,i,2]
        if confidence>conf_threshold:
            x1=int(Detecciones[0,0,i,3]*Ancho_Frame-10)
            y1=int(Detecciones[0,0,i,4]*Alto_Frame-10)
            x2=int(Detecciones[0,0,i,5]*Ancho_Frame+10)
            y2=int(Detecciones[0,0,i,6]*Alto_Frame)
            Cara_Rect.append([x1,y1,x2,y2])
    return frameOpencvDnn,Cara_Rect
Video=cv2.VideoCapture(0)
import time
def cara():
    while True:
        hasFrame,frame=Video.read()
        try:
            resultImg,Cara_Rect=resaltar(Cara_Net,frame)
            faceBox = Cara_Rect[0]
            frame=cv2.rectangle(frame, (faceBox[0],faceBox[1]), (faceBox[2],faceBox[3]),(255,100,100), int(round(resultImg.shape[0]/150)), 8)
            #cv2.imshow("Video",frame)
            if faceBox[0]<200 and faceBox[1]<500:
                ser.write(b"b")
            if faceBox[2]>500 and faceBox[0]>200:
                ser.write(b"v")
            #cv2.waitKey(1)
            time.sleep(.8)
        except:
            rayos=0
################################## EJECUCION #####################################

#################################################################################

mensaje=''
asistenteRespuesta("PiiiiiiiiiIPIPIa, INICIANDO, ¿Como te ayudo?")
import threading
import os
hilo1 = threading.Thread(target=aleatorio)
hilo1.start()
hilo2 = threading.Thread(target=cara)
hilo2.start()
while True:
    print("Escuchando")
    mensaje=input("DIME:")
    #print("DIME:")
    #mensaje=reconocer()
    if mensaje=='apagar':
        ser.write(b'D')
        break
    identificar(mensaje)

asistenteRespuesta("Hasta Luego.")
ser.close()
import sys
os.execl(exit())

