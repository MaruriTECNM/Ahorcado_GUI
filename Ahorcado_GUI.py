#Juego de ahorcado
#Genera una ventana en la cual el usuario tiene que responder una letra, si la letra se encuentra en la palabra a adivinar, se mostrara dicha lecha en pantalla.
#La interfaz fue generada con PyQt5.
#TODO 1: Evitar que el usuario pueda responder con las letras ya dadas como respuesta.
#TODO 2: Implementar la lectura de un archivo importando en lugar de depender de un banco de palabras local.
#TODO 3: Implementar un selector de vidas así como de selector de dificultad con diferentes palabras.
#TODO 4: Implementar palabras con acento asi como evaluación de caracteres especiales.
#Autor(es): Maruri Moguel Ricardo Mauricio (240i0044), Romero Arias Diusty Alejandro (240i0081), Domínguez Fernández Oswaldo Angel (240i0110)
#Institución: TecNM Martinez de la Torre
#Clase: Fundamentos de programación

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout,  QWidget, QLabel, QLineEdit, QPushButton, QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import sys
import random

palabras = [#Lista de palabras
    "Manzana",
    "Pera",
    "Teclado",
    "Silla",
    "Mesa",
    "Cortinas",
    "Butaca",
    "Mochila",
    "Libreta",
    "Zapato",
    "Camisa",
    "Uniforme",
    "Pantalla",
    "Laptop",
    "Alumno",
    "Profesor",
    "Juego",
    "Videojuego",
    "Carro",
    "Moto",
    "Camioneta",
    "Barco",
    "Agua",
    "Lava",
    "Obsidiana"
]

globalVidas=10
globalMaximo=10 #Constante

def llenador(arreglo, tam):#Recibe un arreglo y su tamaño, después, cambia todos sus elementos.
    i = 0
    while i < tam:
        arreglo[i] = "_"#Por guiones bajos.
        i=i+1
    return arreglo#Y se devuelve el arreglo.

def guessCheck(guess, palabra):#Funcion para verificar si letra dada esta bien
    i=0
    while (i<len(palabra)):#Tamaño del arreglo
        if ((guess.lower()==palabra[i]) or (guess.upper()==palabra[i])):#Condicion de mayus o minus
            return 1
        else:
            i+=1
    return 0

def guessFiller(guess,palabra,adivinanza):
    i=0
    while (i<len(palabra)):#Tamaño del arreglo
        if ((guess.lower()==palabra[i]) or (guess.upper()==palabra[i])):#Condicion de mayus o minus
            adivinanza[i]=palabra[i]
        i+=1
    return adivinanza
    
class Ventana(QMainWindow):
    singleton:'Ventana'=None#Singleton garantiza que solo haya una ventana en todo momento.
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ahorcado")#Titulo de la pestaña
        self.texto()#Se llaman a los widgets de texto
        self.botonera()#Y a la botonera
        self.setFixedSize(QSize(300,200))

        layout = QVBoxLayout()#Se implementan los widgets en pantalla
        layout.addWidget(self.text)
        layout.addWidget(self.adivinanza)
        layout.addWidget(self.input)
        layout.addWidget(self.botonJuego)

        widget = QWidget()#Creación del layout de widgets
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        self.show()#Muestra la ventana creada
    
    def texto(self):#Widget de textos
        global globalVidas
        self.Palabra = random.choice(palabras)#Selecciona una palabra al azar del arreglo "palabras"
        self.arrayPalabra = [*self.Palabra]#Guarda la palabra en formato arreglo tal que Hoja -> H, O, J, A
        self.arrayAdivinanza = [*self.Palabra]#Guarda una copia en el segundo arreglo
        self.text = QLabel("Vidas: {}".format(globalVidas))#Muestra las vidas
        
        self.arrayAdivinanza = llenador(self.arrayAdivinanza, len(self.arrayAdivinanza))#Se manda dicha variable a la funcion llenador
        self.adivinanza = QLineEdit()#Se crea un QLineEdit
        self.adivinanza.setEnabled(False)#Y se deshabilita para que el usuario no pueda cambiarlo
        self.adivinanza.setText("{}".format(self.arrayAdivinanza))#Se muestran solo los espacios vacios de la palabra gracias a la funcion llenador
        
        self.input = QLineEdit()#El campo de entrada para el usuario
        self.input.setMaxLength(1)#Maximo de entrada, 1 caracter
        self.input.setValidator(QRegularExpressionValidator(QRegularExpression('[a-zA-Z]+')))#Solo se admiten letras de la A a la Z
    
    def botonera(self):#Widgets de botones
        self.botonJuego = QPushButton("Envia tu letra")#Boton para enviar la letra al programa para verificar si esta bien
        self.botonJuego.clicked.connect(self.juego)#Se conecta este boton con la función juego
    
    
    def juego(self):#Evento de juego
        global globalVidas#Se define como variable global
        guess = str(self.input.text())#Se parsea el texto que esta en self.input y se almacena en "guess"
        if (guessCheck(guess, self.arrayPalabra)==1):#Si la letra es correcta
            self.arrayAdivinanza=guessFiller(guess, self.arrayPalabra, self.arrayAdivinanza)#Se manda a llenar al array vacio
            if (np.array_equal(self.arrayPalabra,self.arrayAdivinanza)==True):#Si ambos arreglos son iguales
                self.input.setMaxLength(100)
                self.input.setValidator(QRegularExpressionValidator(QRegularExpression('[a-zA-Z!¡]+')))
                self.input.setText("¡HAS GANADO!")#Se pone como mensaje de victoria
                self.input.setEnabled(False)#Se deshabilita la entrada de texto
                self.text.setText("La palabra era: {}".format(self.Palabra))#Se muestra la palabra
                self.botonJuego.setText("¿Volver a jugar?")#Se cambia el texto del boton
                self.botonJuego.clicked.connect(self.restart)#Se cambia la funcion del boton a la funcion reset
            else:#Si no son iguales
                self.adivinanza.setText("{}".format(self.arrayAdivinanza))#Se actualiza el texto de la adivinanza
                self.input.setText("")#Y se reinicia el campo de entrada
        else:#Si la letra no es correcta
            globalVidas-=1#Se elimina una vida
            self.input.setText("")#Se reinicia el campo de entrada
            if(globalVidas==0):#Si las vidas son iguales a 0
                self.input.setMaxLength(100)
                self.input.setValidator(QRegularExpressionValidator(QRegularExpression('[a-zA-Z!¡]+')))
                self.input.setText("¡HAS PERDIDO!")#Se pone como mensaje de perder
                self.input.setEnabled(False)#Se deshabilita la entrada de texto
                self.text.setText("La palabra era: {}".format(self.Palabra))#Se muestra la palabra
                self.botonJuego.setText("¿Volver a jugar?")#Se cambia el texto del boton
                self.botonJuego.clicked.connect(self.restart)#Y se cambia la funcion del boton a la funcion reset
            else:#Si aun quedan vidas disponibles
                self.text.setText("Vidas: {}".format(globalVidas))#Se actualiza el contador de vidas
    
    def paintEvent(self, event):#Dibujante
        global globalVidas#Se exporta la variable vidas
        global globalMaximo
        qp = QPainter()
        qp.begin(self)
        if ((float(globalVidas)/float(globalMaximo))<0.90):
                qp.drawEllipse(QPoint(175,25),15,15)#cabeza
        if ((float(globalVidas)/float(globalMaximo))<0.80):                      
                qp.drawLine(175,40,175,80)#torso
        if ((float(globalVidas)/float(globalMaximo))<0.60):
                qp.drawLine(175,45,190,60)#brazo drcho
        if ((float(globalVidas)/float(globalMaximo))<0.40):
                qp.drawLine(175,45,160,60)#brazo izq
        if ((float(globalVidas)/float(globalMaximo))<0.20):
                qp.drawLine(175,80,190,95)#pierna drcha
        if ((float(globalVidas)/float(globalMaximo))<0.10):
                qp.drawLine(175,80,160,95)#pierna izq
        if (globalVidas==0):
                qp.setPen(Qt.red)
                qp.drawEllipse(QPoint(175,25),15,15)#cabeza
                qp.drawLine(175,40,175,80)#torso
                qp.drawLine(175,45,190,60)#brazo drcho
                qp.drawLine(175,45,160,60)#brazo izq
                qp.drawLine(175,80,190,95)#pierna drcha
                qp.drawLine(175,80,160,95)#pierna izq
                qp.drawText(200,40,"¡PERDISTE!")
        qp.end()       
    
    @staticmethod#Se declara como static method para que se pueda invocar la funcion restart() sin tener que volver a invocar la clase Ventana()
    def restart():
        global globalVidas#Se obtiene el numero de vidas actual
        global globalMaximo#Y el maximo
        globalVidas=globalMaximo#Y se actualiza de nuevo para que vuelva al maximo
        Ventana.singleton=Ventana()#Se crea una nueva ventana con singleton, garantizado que solo se cree una ventana.
                    
def main():#La funcion principal
    app=QApplication(sys.argv)#Se crea la aplicacion de PyQt5
    Ventana.restart()#Se manda a llamar la funcion de restart, la cual creara la ventana de PyQt5 a mostrar.
    sys.exit(app.exec())#Ejecuta la aplicacion, se añade sys.exit para que la aplicacion ("app") sea finalizada al cerrar la ventana principal.

if __name__ == '__main__':
    main()#Inicia la funcion principal.