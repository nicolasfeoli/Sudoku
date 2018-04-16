from tkinter import *
import random
import time
import os
from threading import Thread
import tkinter.messagebox
import confSudoku
import confSudoku_support
import pickle
import copy
import sys
import webbrowser


#Coloca una semilla basada en el tiempo actual para que sea mas
# aleatorio.

random.seed(time.time())

################################
class Reloj:

    # The format is padding all the
    timer = [0, 0, 0, 0]
    pattern = '{0:02d}:{1:02d}:{2:02d}'

    # Simple status flag
    # False mean the timer is not running
    # True means the timer is running (counting)
    state = False

    def __init__(self, ventana, color):
        self.ventana = ventana
        self.tiempo = Label(ventana, text="00:00:00", font=("Helvetica", 20), bg=color)
        self.tiempo.grid()

    def update_timeText(self):
        if (self.state):
            self.timer
            #incrementa 1 centisegundo
            self.timer[3] += 1
            # Cada 100 centisegundos es igual a in segundo
            if (self.timer[3] >= 100):
                self.timer[3] = 0
                self.timer[2] += 1
            # Cada 60 segundos es igual a 1 minuto
            if (self.timer[2] >= 60):
                self.timer[1] += 1
                self.timer[2] = 0
            # Cada 60 minutos es igual a 1 hora
            if (self.timer[1] >= 60):
                self.timer[0] += 1
                self.timer[1] = 0
            # We create our time string here
            self.timeString = self.pattern.format(self.timer[0], self.timer[1],
                                                  self.timer[2])
            # Update the timeText Label box with the current time
            self.tiempo.configure(text=self.timeString)
            # Call the update_timeText() function after 1 centisecond
        self.ventana.after(10, self.update_timeText)

    # To start the kitchen timer
    def start(self):
        self.state = True

    # To pause the kitchen timer
    def pause(self):
        self.state = False

    # To reset the timer to 00:00:00
    def reset(self):
        self.timer = [0, 0, 0, 0]
        self.tiempo.configure(text='00:00:00')
        
#############################
        
class Timer:

    # The format is padding all the

    pattern = '{0:02d}:{1:02d}:{2:02d}'

    # Simple status flag
    # False mean the timer is not running
    # True means the timer is running (counting)
    state = False

    def __init__(self, ventana, color, horas, minutos, segundos):
        self.horas = horas
        self.minutos = minutos
        self.segundos = segundos
        self.timer = [horas, minutos, segundos, 0]

        self.ventana = ventana
        self.tiempo = Label(ventana, text=self.pattern.format(self.timer[0],  self.timer[1],
                                                              self.timer[2]), font=("Helvetica", 20), bg=color)
        self.tiempo.grid()

    def update_timeText(self):
        try:
            if (self.state):
                self.timer
                #incrementa 1 centisegundo
                self.timer[3] -= 1
                # Cada 100 centisegundos es igual a in segundo
                if self.timer == [0,0,0,0]:
                    if messagebox.askyesno("Error", "Se termino el tiempo acordado, desea continuar?"):
                        cerrarTimerEmpezarCrono()
                    else:
                        terminarJuego()
                if (self.timer[3] < 0):
                    self.timer[3] = 99
                    self.timer[2] -= 1
                # Cada 60 segundos es igual a 1 minuto
                if (self.timer[2] < 0):
                    self.timer[1] -= 1
                    self.timer[2] = 59
                # Cada 60 minutos es igual a 1 hora
                if (self.timer[1] < 0):
                    self.timer[0] -= 1
                    self.timer[1] = 59
                # We create our time string here
                self.timeString = self.pattern.format(self.timer[0], self.timer[1],
                                                      self.timer[2])
                # Update the timeText Label box with the current time
                self.tiempo.configure(text=self.timeString)
                # Call the update_timeText() function after 1 centisecond
        except Exception:
            pass
        self.ventana.after(10, self.update_timeText)

    # To start the kitchen timer
    def start(self):
        self.state = True

    # To pause the kitchen timer
    def pause(self):
        self.state = False

    # To reset the timer to 00:00:00
    def reset(self):
        self.timer = [self.horas, self.minutos, self.segundos, 0]
        self.tiempo.configure(text='00:00:00')

################################

class Pila:
    def __init__(self):
        self.pila = []
        
    def pop(self):
        try:
            return self.pila.pop()
        except:
            messagebox.showerror("Error", "NO HAY JUGADAS PREVIAS.")
            return None, None

    def push(self, celda):
        self.pila.append(celda)

    def __str__(self):
        return self.pila[::-1]

################################

class SudokuBoard:
    def __init__(self):
        self.clear()

    def clear(self):
        self.grid = [[0 for x in range(9)] for y in range(9)]
        self.locked = []
        self.pila = Pila()

    def getFila(self, row):
        return self.grid[row]

    def getColumna(self, col):
        return [y[col] for y in self.grid]

    def getRegion(self, col, row):
        def make_index(v):
            if v <= 2:
                return 0
            elif v <= 5:
                return 3
            else:
                return 6
        return [y[make_index(col):make_index(col)+3] for y in
                self.grid[make_index(row):make_index(row)+3]]

    def setCelda(self, col, row, v, lock=False):
        if v == self.grid[row][col] or (col, row) in self.locked:
            return
        if v in self.getFila(row):
            raise ValueError("FILA")
        if v in self.getColumna(col):
            raise ValueError("COLUMNA")
        for y in self.getRegion(col, row):
            for x in y:
                if v == x:
                    raise ValueError("REGION")
        self.grid[row][col] = v
        
        if lock:
            self.locked.append((col, row))
        else:
            self.pila.push((row, col))


    def get(self, col, row):
        return self.grid[row][col]


############################################

def sudogen(board):
    board.clear()
    added = [0]
    for y in range(0, 9, 3):
        for x in range(0, 9, 3):
            if len(added) == 10:
                return
            i = 0
            while i in added:
                i = random.randint(1, 9)
            try:
                board.setCelda(random.randint(x, x+2), random.randint(y, y+2),
                          i, lock=True)
            except ValueError:
                pass
            added.append(i)
            

def rgb(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)


colorPanelDict = {"set1":{"fondo":"#DBCF62", "botonesAbajo":"#F5FFB3", "botonesLado":"#FFFFFF", "fondoSudo":"#E3E4E1"},
                  "set2":{"fondo":"#401C64", "botonesAbajo":"#007C99", "botonesLado":"#005F7B", "fondoSudo":"#397C8F"},
                  "set3":{"fondo":"#4491AD", "botonesAbajo":"#7E9DA3", "botonesLado":"#BDC966", "fondoSudo":"#C8D2AC"},
                  "set4":{"fondo":"#4034A9", "botonesAbajo":"#C0003D", "botonesLado":"#31E758", "fondoSudo":"#477E7C"},
                  "set5":{"fondo":"#3C1758", "botonesAbajo":"#E9FF46", "botonesLado":"#7C8320", "fondoSudo":"#8378A7"}}

###############################################

class SudokuGUI(Frame):
    board_generator = staticmethod(sudogen)
    
    dictTipos = {"num":{ 0:"", 1:"1", 2:"2",  3:"3",  4:"4",   5:"5", 6:"6",  7:"7",   8:"8",    9:"9"  },
                 "let":{ 0:"", 1:"A", 2:"B",  3:"C",  4:"D",   5:"E", 6:"F",  7:"G",   8:"H",    9:"I"  },
                 "rom":{ 0:"", 1:"I", 2:"II", 3:"III", 4:"IV", 5:"V", 6:"VI", 7:"VII", 8:"VIII", 9:"IX" },
                 "col":{ 1:rgb(0,   0,   255), 2:rgb(255, 0, 0),   3:rgb(0,   128,   0), 4:rgb(255, 255, 0),
                         5:rgb(128, 0,   128), 6:rgb(0,   0, 0),   7:rgb(144, 238, 144), 8:rgb(255, 165, 0),
                         9:rgb(255, 115, 139), 0:rgb(128, 128, 128) }}

    teclaActual = None

    def new_game(self):
        self.board.clear()
        self.board_generator(self.board)
        self.sync_board_and_canvas()

    def make_modal_window(self, title):
        window = Toplevel()
        window.title(title)
        window.attributes('-topmost', True)
        window.grab_set()
        window.focus_force()
        return window

    def load_game(self):
        with open("sudoku2016juegoactual.dat", 'rb') as f:
            board = pickle.load(f)
            self.board = board
        self.sync_board_and_canvas()


        window.mainloop()

    def save_game(self):
        with open("sudoku2016juegoactual.dat", 'wb') as f:
            pickle.dump(self.board, f)#, protocol=2)
            f.close()



    def make_grid(self):
        c = Canvas(self, bg=colorPanelDict[confSudoku_support.colorPanel]["fondoSudo"], width='512', height='512')
        c.pack(side='top', fill='both', expand='1')

        self.rects   = [[None for x in range(9)] for y in range(9)]
        self.handles = [[None for x in range(9)] for y in range(9)]
        rsize = 512/9
        guidesize = 512/3

        for y in range(9):
            for x in range(9):
                (xr, yr) = (x*guidesize, y*guidesize)
                self.rects[y][x] = c.create_rectangle(xr, yr, xr+guidesize,
                                                      yr+guidesize, width=3)
                (xr, yr) = (x*rsize, y*rsize)
                r = c.create_rectangle(xr, yr, xr+rsize, yr+rsize)
                t = c.create_text(xr+rsize/2, yr+rsize/2, text="SUDO",
                                  font="System 15 bold")
                self.handles[y][x] = (r, t)

        self.canvas = c
        self.sync_board_and_canvas()


    def sync_board_and_canvas(self):
        #La idea era que las ponga de otro color si estan bloqueadas, pero no funciona :: poner un if
        print("pasa por sync_board")
        g = self.board.grid
        if confSudoku_support.tipoJuego.get() == "num":
            for y in range(9):
                for x in range(9):
                    self.canvas.itemconfig(self.handles[y][x][1],
                                           text=self.dictTipos["num"][g[y][x]])
        if confSudoku_support.tipoJuego.get() == "let":
            for y in range(9):
                for x in range(9):
                    self.canvas.itemconfig(self.handles[y][x][1],
                                           text=self.dictTipos["let"][g[y][x]])
        if confSudoku_support.tipoJuego.get() == "rom":
            for y in range(9):
                for x in range(9):
                    self.canvas.itemconfig(self.handles[y][x][1],
                                           text=self.dictTipos["rom"][g[y][x]])

        if confSudoku_support.tipoJuego.get() == "col":
            for y in range(9):
                for x in range(9):
                    self.canvas.itemconfig(self.handles[y][x][0],
                                           fill=self.dictTipos["col"][g[y][x]])
                    self.canvas.itemconfig(self.handles[y][x][1],
                                           text="")
            self.tirarLineasGrandes()
        for i in board.grid:
            for k in i:
                if k == 0:
                    return
        juegoTerminado()
                

    def tirarLineasGrandes(self):
        guidesize = 512/3
        for y in range(9):
            for x in range(9):
                (xr, yr) = (x*guidesize, y*guidesize)
                self.rects[y][x] = self.canvas.create_rectangle(xr, yr,
                                                                xr+guidesize,
                                                                yr+guidesize,
                                                                width=3)
                

    def canvas_click(self, event):
        print("Click! (%d,%d)" % (event.x, event.y))
        self.canvas.focus_set()
        rsize = 512/9
        (x,y) = (0, 0)
        if event.x > rsize:
            x = int(event.x/rsize)
        if event.y > rsize:
            y = int(event.y/rsize)
        print(x,y)
        if self.current:
            (tx, ty) = self.current
        self.current = (x,y)
        try:
            self.canvas_key(self.teclaActual)
        except ValueError:
            print("No hay valor asignado aun.")
            messagebox.showerror("Error", "FALTA QUE SELECCIONE EL ELEMENTO.")
            pass

    def canvas_key(self, char):
        if not(char):
            raise ValueError
        if char.isdigit() and int(char) > 0 and self.current:
            (x,y) = self.current
            try:
                self.board.setCelda(x, y, int(char))
                self.sync_board_and_canvas()
            except ValueError as e:
                messagebox.showerror("Error", "JUGADA NO ES VÁLIDA PORQUE EL ELEMENTO YA ESTÁ EN LA %s"%e)

    def setTeclaActual(self, teclaNueva):
        self.teclaActual = teclaNueva

    def __init__(self, master, board):
        Frame.__init__(self, master)

        #if master:
            #master.title("SudokuGUI")

        self.board = board
        self.board_generator(board)

        self.make_grid()
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.current = None
        self.pack()


###############################################################

def siguienteCampo(grid, i, j):
    for k in range(i,9):
        for l in range(j,9):
            if grid[k][l] == 0:
                    return k,l
    for k in range(0,9):
        for l in range(0,9):
            if grid[k][l] == 0:
                return k,l
    return None, None


def valida(grid, i, j, e):
    if all([e != grid[i][m] for m in range(9)]): #si el valor esta en la fila
        if all([e != grid[m][j] for m in range(9)]): #si el valor esta en la columna
            regionX, regionY = 3 *(i//3), 3 *(j//3)#saca la region en la que esta la celda
            for m in range(regionX, regionX+3):
                for n in range(regionY, regionY+3):
                    if grid[m][n] == e:
                        return False #retorna False si el valor esta en la region
            return True
    return False


def solucionaSudoku(grid, i=0, j=0):
    i,j = siguienteCampo(grid, i, j)
    if i == None:
        return True
    for e in range(1,10):
        if valida(grid, i, j, e):
            grid[i][j] = e
            if solucionaSudoku(grid, i, j):
                return True
            # resetea la celda actual
            grid[i][j] = 0
    return False


def juegoTerminado():
    global reloj, juegoIniciado, resuelto
    juegoIniciado = False
    reloj.pause()
    if not(resuelto):
        insertaTop10()
    messagebox.showinfo("Fin", "Siguiente nivel")
    juegoNuevo()
        

def borrarSudoku():
    global board, tablaInicial, tablaInicial,reloj
    board.grid = copy.deepcopy(tablaInicial)
    tablero.sync_board_and_canvas()
    reloj.reset()


def resolverSudokuNormal():
    global board, tablero, tablaResuelta, resuelto
    resuelto = True
    board.grid = copy.deepcopy(tablaResuelta)
    tablero.sync_board_and_canvas()


def desplegarAcercaDe():
    pass


def ayuda():
    try:
        if sys.platform == "linux":
            webbrowser.open_new(r'./manual_de_usuario.mp4')
        else:
            os.startfile("manual_de_usuario.mp4")
    except Exception as e:
        print(e)
        nada()


def terminarJuego():
    global reloj, juegoIniciado, nivel
    reloj.pause()
    if confSudoku_support.mutinivel:
        nivel += 1
    if messagebox.askyesno("Terminar", "Desea terminar el juego?"):
        juegoIniciado = False
        juegoNuevo()
    else:
        reloj.start()


def cerrarTimerEmpezarCrono():
    global reloj, marcoReloj, hilo
    reloj.tiempo.destroy()
    del(reloj)
    reloj = Reloj(marcoReloj, colorPanelDict[confSudoku_support.colorPanel]["fondo"])
    startReloj()


def onClickBtn(tecla):
    global botones,tablero
    normalizarBotones()
    num = int(tecla)-1
    botones[num].configure(underline=0)
    botones[num].flash()
    tablero.setTeclaActual(tecla)


def startReloj():
    global hilo, reloj
    reloj.update_timeText()
    hilo = Thread(target=reloj.start, args=())
    hilo.start()
    reloj.pause()
    reloj.reset()

def guarda():
    pass

def cargaTop10():
    global top10
    try:
        with open("sudoku2016top10.dat", 'rb') as f:
            top10 = pickle.load(f)
            f.close()
    except Exception:
        top10 = []


def salvaTop10(self):
    with open("sudoku2016top10.dat", 'wb') as f:
        pickle.dump(top10, f)#, protocol=2)
        f.close()

def insertaTop10():
    global top10, reloj
    if top10 == []:
        top10 += [(confSudoku_support.nombreJugador.get(), getTiempo(reloj))]
    for i in top10:
        pass

    
def getTiempo(reloj):
    if confSudoku_support.tipoTiempo.get() == "2" and isinstance(reloj, Reloj):
        tiempo = str(int(confSudoku_support.horas.get())+reloj.timer[0])+str(int(confSudoku_support.minutos.get())+reloj.timer[1])+str(int(confSudoku_support.segundos.get())+reloj.timer[2])
        return tiempo
    if confSudoku_support.tipoTiempo.get() == "2":
        tiempo =  str(int(confSudoku_support.horas.get())-reloj.timer[0])+str(int(confSudoku_support.minutos.get())-reloj.timer[1])+str(int(confSudoku_support.segundos.get())-reloj.timer[2])
        return tiempo
    tiempo =  str(reloj.timer[0])+str(reloj.timer[1])+str(reloj.timer[2])
    return tiempo
        
    
def normalizarBotones():
    global botones, tipoJuego
    for i in botones:
        i.configure(state=NORMAL, underline=-1)


def juegoNuevo():
    global tablero, tablaInicial, board, reloj, botones, juegoIniciado, tablaResuelta
    if juegoIniciado:
        messagebox.showerror("ERROR", "El juego ya esta iniciado.")
    else:
        normalizarBotones()
        tablero.new_game()
        tablaInicial  = copy.deepcopy(board.grid)
        tablaResuelta = copy.deepcopy(tablaInicial)
        solucionaSudoku(tablaResuelta)
        reloj.reset()
        reloj.start()
        juegoIniciado = True


def hacerMenu(root):
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Iniciar juego")#, command=pass)
    filemenu.add_command(label="Cargar juego")#, command=pass)
    filemenu.add_command(label="Guardar juego actual", command=tablero.save_game)
    filemenu.add_command(label="Top 10")
    filemenu.add_command(label="Reiniciar", command=juegoNuevo)
    filemenu.add_command(label="Terminar juego")#, command=pass)
    filemenu.add_separator()
    filemenu.add_command(label="Salir", command=root.destroy)
    menubar.add_cascade(label="Juego", menu=filemenu)

    vermenu = Menu(menubar, tearoff=0)
    vermenu.add_command(label="Top 10")
    vermenu.add_command(label="Ver partidas",command=ayuda)
    vermenu.add_separator()
    vermenu.add_command(label="Configuraciones")
    menubar.add_cascade(label="Configuraciones", menu=vermenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Manual de Usuario", command=ayuda)
    helpmenu.add_command(label="Acerca de..", command=desplegarAcercaDe)
    menubar.add_cascade(label="Ayuda", menu=helpmenu)

    root.config(menu=menubar)


def generarBotones():
    global botones, marcoBotones, tipoJuego
    botones = [None for i in range(9)]
    tipoJuego = confSudoku_support.tipoJuego.get()
    if tipoJuego == "col":
        for i in range(1,10):
            exec("botones[%d] = Button(marcoBotones, command=lambda: onClickBtn(\"%d\"),\
                                       bg=\"%s\", width=10, bd=10, pady=9, state=DISABLED)"\
                                       %(i-1, i, tablero.dictTipos[tipoJuego][i]))
            exec("botones[%d].pack()"%(i-1))
    else:
        for i in range(1,10):
            exec("botones[%d] = Button(marcoBotones, command=lambda: onClickBtn(\"%d\"),\
                                       text=\"%s\", bg=\"%s\", font=\"System 13 bold\", width=10, bd=10, pady=5, state=DISABLED)"\
                                       %(i-1, i, tablero.dictTipos[tipoJuego][i],
                                         colorPanelDict[confSudoku_support.colorPanel]["botonesLado"]))
            exec("botones[%d].pack()"%(i-1))


def pruebaPila():
    global board
    (x,y) = board.pila.pop()
    if x != None:
        board.grid[x][y] = 0
        tablero.sync_board_and_canvas()


def prueba():
    global board
    print(board)


def registra():
    global root, board, tablero
    board.clear()
    tablero.sync_board_and_canvas()
    botonesRegistra = []
    marcoOpciones = Label(root, width=150, height=30, bg=colorPanelDict[confSudoku_support.colorPanel]["fondo"])
    marcoOpciones.place(x=10,y=565)
    botonesRegistra += [Button(root, bg=colorPanelDict[confSudoku_support.colorPanel]["botonesAbajo"], text="Registrar", command=lambda: guarda())]
    botonesRegistra += [Button(root, bg=colorPanelDict[confSudoku_support.colorPanel]["botonesAbajo"], text="Generar Sudoku", command=lambda: genera())]
    botonesRegistra[0].place(x=50,y=570)
    botonesRegistra[1].place(x=200,y=570)



def genera():
    global board, tablero
    tablero.new_game()



def armarTablero(a_tipoJuego, a_ladoPanel, a_tipoTiempo):
    global marcoBotones, marcoReloj, tablero, marcoMedio, board, root, tipoJuego,\
           ladoPanel, tipoTiempo, tablaInicial, reloj, juegoIniciado

    juegoIniciado = False
    root = Tk()
    root.wm_title("Sudoku")
    root.geometry("1000x800")

    marcoFondo = Label(root, bg=colorPanelDict[confSudoku_support.colorPanel]["fondo"], height=100, width=300)
    marcoFondo.place(relx=0,rely=0)

    marcoMedio = Frame(root)
    marcoBotones = Frame(root)
    marcoReloj = LabelFrame(root, labelanchor="nw",text="Reloj", bg=colorPanelDict[confSudoku_support.colorPanel]["fondo"])
    if confSudoku_support.tipoTiempo.get() == "2":
        reloj = Timer(marcoReloj, colorPanelDict[confSudoku_support.colorPanel]["fondo"], int(confSudoku_support.horas.get()),
                      int(confSudoku_support.minutos.get()), int(confSudoku_support.segundos.get()))
    elif confSudoku_support.tipoTiempo.get() == "1":
        reloj = Reloj(marcoReloj, colorPanelDict[confSudoku_support.colorPanel]["fondo"])
    board = SudokuBoard()
    tablero = SudokuGUI(marcoMedio, board)
    board.clear()
    tablero.sync_board_and_canvas()

    nombreJugador = confSudoku_support.nombreJugador.get()

    labelNombre = Label(root, text=nombreJugador, font="System 12 bold", bg=colorPanelDict[confSudoku_support.colorPanel]["fondo"])
    labelNombre.place(x=10, y=650)

    nivel = confSudoku_support.nivel.get()

    Label(root, text="Sudoku 2.0", font="System 19 bold", bg=colorPanelDict[confSudoku_support.colorPanel]["fondo"]).pack(side=TOP)
    
    tablaInicial  = []
    tablaResuelta = []
    
    botonesAbajo = []
    botonesAbajo += [Button(root, bg=colorPanelDict[confSudoku_support.colorPanel]["botonesAbajo"], text="Borrar Juego!", command=borrarSudoku)]
    botonesAbajo += [Button(root, bg=colorPanelDict[confSudoku_support.colorPanel]["botonesAbajo"], text="Resolver", command=lambda: resolverSudokuNormal())]
    botonesAbajo += [Button(root, bg=colorPanelDict[confSudoku_support.colorPanel]["botonesAbajo"], text="Borrar Jugada", command=lambda: pruebaPila())]
    botonesAbajo += [Button(root, bg=colorPanelDict[confSudoku_support.colorPanel]["botonesAbajo"], text="Terminar Juego", command=lambda: terminarJuego())]
    botonesAbajo += [Button(root, bg=colorPanelDict[confSudoku_support.colorPanel]["botonesAbajo"], text="Iniciar Juego", command=lambda: juegoNuevo())]
    botonesAbajo += [Button(root, bg=colorPanelDict[confSudoku_support.colorPanel]["botonesAbajo"], text="Registrar Partida", command=lambda: registra())]

    botonesAbajo[0].place(x=190,y=570)
    botonesAbajo[1].place(x=320,y=570)
    botonesAbajo[2].place(x=400,y=570)
    botonesAbajo[3].place(x=400,y=600)
    botonesAbajo[4].place(x=190,y=600)
    botonesAbajo[5].place(x=190,y=640)

    marcoBotones = Frame(root)
    botones = []

    generarBotones()

    if confSudoku_support.ladoPanel.get() == "izq":
        marcoMedio.place(x=50,y=50)
        marcoBotones.place(x=700, y=50)
    else:
        marcoMedio.place(x=400,y=50)
        marcoBotones.place(x=50, y=50)

    hacerMenu(root)

    marcoReloj.place(x=10,y=570)
    startReloj()

############################################
    
if __name__ == "__main__":
    ventConf = Tk()
    confSudoku_support.set_Tk_var()
    top = confSudoku.ConfSudoku(ventConf)
    confSudoku_support.init(ventConf, top)
    ventConf.mainloop()
