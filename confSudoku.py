#! /usr/bin/env python
#
# GUI module generated by PAGE version 4.7
# In conjunction with Tcl version 8.6
#    Jun 10, 2016 11:45:35 PM
import sys
import sudoku
import tkinter.messagebox

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

import confSudoku_support

def vp_start_gui():
    '''Starting point when module is the sudoku routine.'''
    global val, w, root
    root = Tk()
    confSudoku_support.set_Tk_var()
    top = ConfSudoku(root)
    confSudoku_support.init(root, top)
    root.sudokuloop()

w = None
def create_ConfSudoku(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    confSudoku_support.set_Tk_var()
    top = ConfSudoku (w)
    confSudoku_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_ConfSudoku():
    global w
    w.destroy()
    w = None


class ConfSudoku:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        font10 = "-family {DejaVu Sans} -size -12 -weight normal "  \
            "-slant roman -underline 0 -overstrike 0"
        font11 = "-family {DejaVu Sans Mono} -size -12 -weight normal "  \
            "-slant roman -underline 0 -overstrike 0"

        top.geometry("649x379+385+154")
        top.title("New Toplevel 1")
        

        self.labelFrameJuego = LabelFrame(top)
        self.labelFrameJuego.place(x=40, y=70, height=295, width=200)
        self.labelFrameJuego.configure(relief=GROOVE)
        self.labelFrameJuego.configure(text='''Juego''')
        self.labelFrameJuego.configure(width=200)
        
        self.Label5 = Label(self.labelFrameJuego)
        self.Label5.place(relx=0.05, y=5, height=39, width=66)
        self.Label5.configure(activebackground="#f9f9f9")
        self.Label5.configure(text="Nombre\nJugador:")
        self.Label5.configure(width=66)

        self.Entry4 = Entry(self.labelFrameJuego)
        self.Entry4.place(x=80, y=20, height=21, width=106)
        self.Entry4.configure(background="white")
        self.Entry4.configure(font=font11)
        self.Entry4.configure(width=106, textvariable=confSudoku_support.nombreJugador)
        
        def cambiarMultinivel():
            confSudoku_support.multinivel = not(confSudoku_support.multinivel)
            if confSudoku_support.multinivel: 
                self.barraDificultad.configure(state=DISABLED, relief=SUNKEN)
            else:
                self.barraDificultad.configure(state=NORMAL, relief=FLAT)
        
        self.multi = Checkbutton(self.labelFrameJuego)
        self.multi.place(x=80, y=55)
        self.multi.configure(command=lambda: cambiarMultinivel(), text="Multinivel")

        self.barraDificultad = Scale(self.labelFrameJuego)
        self.barraDificultad.place(relx=0.4, rely=0.29, relwidth=0.52,
                                   relheight=0.0, height=40)
        self.barraDificultad.configure(activebackground="#d9d9d9")
        self.barraDificultad.configure(font=font10)
        self.barraDificultad.configure(orient="horizontal")
        self.barraDificultad.configure(troughcolor="#d9d9d9")
        self.barraDificultad.configure(from_=1, to=3, variable=confSudoku_support.nivel)
        self.barraDificultad.configure(tickinterval=1)

        self.Label1 = Label(self.labelFrameJuego)
        self.Label1.place(relx=0.05, rely=0.36, height=19, width=66)
        self.Label1.configure(text='''Dificultad:''')
        self.Label1.configure(width=66)

        self.marcoTipos = Frame(self.labelFrameJuego)
        self.marcoTipos.place(x=80, y=150, height=105, width=105)
        self.marcoTipos.configure(relief=GROOVE)
        self.marcoTipos.configure(borderwidth="2")
        self.marcoTipos.configure(relief=GROOVE)
        self.marcoTipos.configure(width=105)

        self.radioNumeros = Radiobutton(self.marcoTipos)
        self.radioNumeros.place(x=10, y=10, height=21, width=83)
        self.radioNumeros.configure(activebackground="#d9d9d9")
        self.radioNumeros.configure(justify=LEFT)
        self.radioNumeros.configure(text='''Numeros''')
        self.radioNumeros.configure(value="num")
        self.radioNumeros.configure(variable=confSudoku_support.tipoJuego)

        self.radioColores = Radiobutton(self.marcoTipos)
        self.radioColores.place(x=10, y=30, height=21, width=72)
        self.radioColores.configure(activebackground="#d9d9d9")
        self.radioColores.configure(justify=LEFT)
        self.radioColores.configure(text='''Colores''')
        self.radioColores.configure(value="col")
        self.radioColores.configure(variable=confSudoku_support.tipoJuego)

        self.radioLetras = Radiobutton(self.marcoTipos)
        self.radioLetras.place(x=10, y=50, height=21, width=66)
        self.radioLetras.configure(activebackground="#d9d9d9")
        self.radioLetras.configure(justify=LEFT)
        self.radioLetras.configure(text='''Letras''')
        self.radioLetras.configure(value="let")
        self.radioLetras.configure(variable=confSudoku_support.tipoJuego)

        self.radioRoma = Radiobutton(self.marcoTipos)
        self.radioRoma.place(x=10, y=70, height=21, width=63)
        self.radioRoma.configure(activebackground="#d9d9d9")
        self.radioRoma.configure(justify=LEFT)
        self.radioRoma.configure(text='''Roma''')
        self.radioRoma.configure(value="rom")
        self.radioRoma.configure(variable=confSudoku_support.tipoJuego)

        self.Message1 = Message(self.labelFrameJuego)
        self.Message1.place(x=10, y=140, height=38, width=62)
        self.Message1.configure(text='''Tipo de 
Juego:''')
        self.Message1.configure(width=70)

        self.labelFrameApariencia = LabelFrame(top)
        self.labelFrameApariencia.place(x=260, y=70, height=295, width=180)
        self.labelFrameApariencia.configure(relief=GROOVE)
        self.labelFrameApariencia.configure(text='''Apariencia''')
        self.labelFrameApariencia.configure(width=180)

        self.Label2 = Label(self.labelFrameApariencia)
        self.Label2.place(relx=0.17, rely=0.11, height=19, width=96)
        self.Label2.configure(text='''Lado del panel:''')

        self.radioDerecha = Radiobutton(self.labelFrameApariencia)
        self.radioDerecha.place(x=90, y=60, height=21, width=79)
        self.radioDerecha.configure(activebackground="#d9d9d9")
        self.radioDerecha.configure(justify=LEFT)
        self.radioDerecha.configure(text='''Derecha''')
        self.radioDerecha.configure(value="der")
        self.radioDerecha.configure(variable=confSudoku_support.ladoPanel)

        self.radioIzquierda = Radiobutton(self.labelFrameApariencia)
        self.radioIzquierda.place(x=10, y=60, height=21, width=85)
        self.radioIzquierda.configure(activebackground="#d9d9d9")
        self.radioIzquierda.configure(justify=LEFT)
        self.radioIzquierda.configure(text='''Izquierda''')
        self.radioIzquierda.configure(value="izq")
        self.radioIzquierda.configure(variable=confSudoku_support.ladoPanel)

        self.Button1 = Button(self.labelFrameApariencia)
        self.Button1.place(relx=0.56, rely=0.44, height=27, width=67)
        self.Button1.configure(activebackground="#d9d9d9")
        self.esto5 = PhotoImage(file="esto.gif")
        self.Button1.configure(image=self.esto5, command=lambda: cambiarColor("set5"))

        self.Button2 = Button(self.labelFrameApariencia)
        self.Button2.place(relx=0.56, rely=0.62, height=27, width=67)
        self.Button2.configure(activebackground="#d9d9d9")
        self.esto = PhotoImage(file="esto.gif")
        self.Button2.configure(image=self.esto, command=lambda: cambiarColor("set1"))

        self.Button3 = Button(self.labelFrameApariencia)
        self.Button3.place(relx=0.56, rely=0.8, height=27, width=67)
        self.Button3.configure(activebackground="#d9d9d9")
        self.esto2 = PhotoImage(file="esto2.gif")
        self.Button3.configure(image=self.esto2, command=lambda: cambiarColor("set2"))

        self.Button4 = Button(self.labelFrameApariencia)
        self.Button4.place(relx=0.06, rely=0.62, height=27, width=67)
        self.Button4.configure(activebackground="#d9d9d9")
        self.esto3 = PhotoImage(file="esto3.gif")
        self.Button4.configure(image=self.esto3, command=lambda: cambiarColor("set3"))

        self.Button5 = Button(self.labelFrameApariencia)
        self.Button5.place(relx=0.06, rely=0.8, height=27, width=67)
        self.Button5.configure(activebackground="#d9d9d9")
        self.esto4 = PhotoImage(file="esto4.gif")
        self.Button5.configure(image=self.esto4, command=lambda: cambiarColor("set4"))

        self.Message2 = Message(self.labelFrameApariencia)
        self.Message2.place(x=10, y=110, height=38, width=66)
        self.Message2.configure(text='''Color del
Tablero:''')
        self.Message2.configure(width=70)

        self.labelFrameTiempo = LabelFrame(top)
        self.labelFrameTiempo.place(x=460, y=70, height=215, width=150)
        self.labelFrameTiempo.configure(relief=GROOVE)
        self.labelFrameTiempo.configure(text='''Tiempo''')
        self.labelFrameTiempo.configure(width=150)

        self.Entry1 = Entry(self.labelFrameTiempo)
        self.Entry1.place(x=40, y=165, height=21, width=26)
        self.Entry1.configure(background="white")
        self.Entry1.configure(font=font11)
        self.Entry1.configure(width=26, state=DISABLED, justify=CENTER, textvariable=confSudoku_support.horas)

        self.Entry2 = Entry(self.labelFrameTiempo)
        self.Entry2.place(x=70, y=165, height=21, width=26)
        self.Entry2.configure(background="white")
        self.Entry2.configure(font=font11)
        self.Entry2.configure(width=26,state=DISABLED, justify=CENTER, textvariable=confSudoku_support.minutos)

        self.Entry3 = Entry(self.labelFrameTiempo)
        self.Entry3.place(x=100, y=165, height=21, width=26)
        self.Entry3.configure(background="white")
        self.Entry3.configure(font=font11)
        self.Entry3.configure(width=26, state=DISABLED, justify=CENTER, textvariable=confSudoku_support.segundos)

        self.radioCronometro = Radiobutton(self.labelFrameTiempo)
        self.radioCronometro.place(x=20, y=70, height=21, width=100)
        self.radioCronometro.configure(activebackground="#d9d9d9")
        self.radioCronometro.configure(justify=LEFT)
        self.radioCronometro.configure(text='''Cronometro''')
        self.radioCronometro.configure(value="1")
        self.radioCronometro.configure(command=self.deshabilitarEntradas)
        self.radioCronometro.configure(variable=confSudoku_support.tipoTiempo)

        self.radioTemporizador = Radiobutton(self.labelFrameTiempo)
        self.radioTemporizador.place(x=20, y=100, height=21, width=111)
        self.radioTemporizador.configure(activebackground="#d9d9d9")
        self.radioTemporizador.configure(justify=LEFT)
        self.radioTemporizador.configure(text='''Temporizador''')
        self.radioTemporizador.configure(value="2")
        self.radioTemporizador.configure(command=self.habilitarEntradas)
        self.radioTemporizador.configure(variable=confSudoku_support.tipoTiempo)

        self.radioSinTemp = Radiobutton(self.labelFrameTiempo)
        self.radioSinTemp.place(x=20, y=40, height=21, width=94)
        self.radioSinTemp.configure(activebackground="#d9d9d9")
        self.radioSinTemp.configure(justify=LEFT)
        self.radioSinTemp.configure(text='''Sin tiempo''')
        self.radioSinTemp.configure(value="0")
        self.radioSinTemp.configure(command=self.deshabilitarEntradas)
        self.radioSinTemp.configure(variable=confSudoku_support.tipoTiempo)

        self.Label4 = Label(self.labelFrameTiempo)
        self.Label4.place(relx=0.07, rely=0.65, height=34, width=90)
        self.Label4.configure(text='''Tiempo del 
Temporizador:''')

        self.Label3 = Label(top)
        self.Label3.place(relx=0.15, rely=0.05)#, height=19, width=159)
        self.Label3.configure(text="Configuracion del Sudoku")
        self.Label3.configure(font="Helvetica 20")
        
        
        self.Button6 = Button(top)
        
        def cambiarColor(nom):
            confSudoku_support.colorPanel=nom
        
        def limpiarVentana():
            if confSudoku_support.horas.get().isdigit() and confSudoku_support.minutos.get().isdigit() and confSudoku_support.segundos.get().isdigit() and len(confSudoku_support.horas.get()) <= 2 and len(confSudoku_support.minutos.get()) <= 2 and len(confSudoku_support.segundos.get()) <= 2 and len(confSudoku_support.nombreJugador.get()) >= 2 and len(confSudoku_support.nombreJugador.get()) <= 25:
                top.destroy()
                sudoku.armarTablero(confSudoku_support.tipoJuego, confSudoku_support.ladoPanel, confSudoku_support.tipoTiempo)
            else:
                messagebox.showerror("ERROR", "Hay un problema con el nombre del jugador o con el tiempo ingresado")
            
        self.Button6.place(relx=0.71, rely=0.77, height=77, width=176)
        self.Button6.configure(activebackground="#d9d9d9")
        self.Button6.configure(text='''Empezar el Juego!~''')
        self.Button6.configure(width=176)
        self.Button6.configure(command=limpiarVentana)
    
        #self.top.pack()
        
    def habilitarEntradas(self):
        self.Entry1.configure(state=NORMAL)
        self.Entry2.configure(state=NORMAL)
        self.Entry3.configure(state=NORMAL)
            
    def deshabilitarEntradas(self):
        self.Entry1.configure(state=DISABLED)
        self.Entry2.configure(state=DISABLED)
        self.Entry3.configure(state=DISABLED)

        
if __name__ == '__main__':
    vp_start_gui()



