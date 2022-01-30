import tkinter
from tkinter import *
from PIL import Image, ImageTk
import threading
import traductor
thread = None
theTraductor = None
import sys 

def iniciar():
    global thread
    global theTraductor
    theTraductor = traductor.Traductor()
    thread = threading.Thread(target=theTraductor.run,args=[])
    thread.start()

def terminar():
    global theTraductor
    theTraductor.terminarPrograma()

class Window(Frame):
    def init(self, master=None):
        Frame.init(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)

        load = Image.open("mano.jpg")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)


ventana = tkinter.Tk()
ventana.geometry("400x400")
ventana.title('G-CONTROL')
app = Window(ventana)
ventana.resizable(0, 0)
#ventana.iconbitmap('Mano.ico')


botonApagar = Button(ventana, text = "APAGAR", height = 2, bg = "red", fg = "white", command=lambda:terminar())
botonApagar.pack(side=BOTTOM,fill=BOTH)

botonEncender = Button(ventana, text = "ACTIVAR",  height = 2, bg = "green", fg = "white", command = lambda:iniciar())
botonEncender.pack(side=BOTTOM, fill=BOTH, pady=3)

etiqueta = tkinter.Label(ventana, text = "G-CONTROL")
etiqueta.pack(side=TOP, fill=BOTH, pady=3)


ventana.mainloop()
sys.exit()