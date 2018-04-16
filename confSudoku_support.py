#! /usr/bin/env python
#
# Support module generated by PAGE version 4.7
# In conjunction with Tcl version 8.6
#    Jun 10, 2016 11:38:58 PM


import sys

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

def set_Tk_var():
    # These are Tk variables used passed to Tkinter and must be
    # defined before the widgets using them are created.
    global ladoPanel
    ladoPanel = StringVar()
    ladoPanel.set("izq")

    global tipoTiempo
    tipoTiempo = StringVar()
    tipoTiempo.set("1")
    
    global colorPanel
    colorPanel = "set1"
    
    global segundos
    segundos = StringVar()
    segundos.set("0")
    
    global minutos
    minutos = StringVar()
    minutos.set("0")
    
    global horas
    horas = StringVar()
    horas.set("0")
    
    global tipoJuego
    tipoJuego = StringVar()
    tipoJuego.set("num")
    
    global nivel
    nivel = IntVar()
    nivel.set(1)
    
    global nombreJugador
    nombreJugador = StringVar()
    nombreJugador.set("")
    
    global multinivel
    multinivel = False

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import confSudoku
    confSudoku.vp_start_gui()


