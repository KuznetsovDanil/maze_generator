from tkinter import *
from tkinter.ttk import Radiobutton
from importlib import reload
import linewalls
import squarewalls
import maze


# обновление максимальных значений координат
# в зависимости от размеров лабиринта
def update_spinbox(*args):
    spin5['to'] = var1.get()
    spin6['to'] = var2.get()


# обновление характеристик лабиринта
def update_maze():
    reload(maze)
    maze.set_maze(var1.get(), var2.get(), var3.get(), chk_state.get(),
                  var4.get(), (var5.get()-1, var6.get()-1), generation.get(),
                  pathfinding.get(), var7.get())
    return


# создание лабиринта с тонкими стенами
def clicked1():
    update_maze()
    linewalls.configure()
    linewalls.run()


# создание лабиринта с объёмными стенами
def clicked2():
    update_maze()
    squarewalls.run()


# графический интерфейс программы
window = Tk()
window.title("Лабиринт")
window.geometry("500x350")
lbl1 = Label(window, text="Ширина:", font=("Calibri", 12))
lbl2 = Label(window, text="Высота:", font=("Calibri", 12))
lbl3 = Label(window, text="Размер клетки:", font=("Calibri", 12))
lbl1.grid(column=0, row=0, padx=(54, 0))
lbl2.grid(column=0, row=1, padx=(60, 0))
lbl3.grid(column=0, row=3, padx=(10, 0))
var1, var2, var3 = IntVar(), IntVar(), IntVar()
var1.set(30)
var2.set(25)
var3.set(30)
spin1 = Spinbox(window, from_=5, to=150, width=5, textvariable=var1)
spin2 = Spinbox(window, from_=5, to=100, width=5, textvariable=var2)
spin3 = Spinbox(window, from_=5, to=100, width=5, textvariable=var3)
spin1.grid(column=1, row=0)
spin2.grid(column=1, row=1)
spin3.grid(column=1, row=3)
chk_state = BooleanVar()
chk_state.set(True)
chk = Checkbutton(window, text="Включить анимацию", font=("Calibri", 12), variable=chk_state, padx=20)
chk.grid(column=0, row=4, columnspan=2, pady=(20, 0))
lbl4 = Label(window, text="Частота кадров:", font=("Calibri", 12), padx=20)
lbl4.grid(column=0, row=5)
var4 = IntVar()
var4.set(60)
spin4 = Spinbox(window, from_=10, to=100, width=5, textvariable=var4)
spin4.grid(column=1, row=5)
lbl5 = Label(window, text="Стартовая клетка:", font=("Calibri", 12))
lbl5.grid(column=0, row=7, columnspan=2, padx=(20, 0))
var5, var6 = IntVar(), IntVar()
var5.set(1)
var6.set(1)
spin5 = Spinbox(window, from_=1, to=var1.get(), width=5, textvariable=var5)
spin6 = Spinbox(window, from_=1, to=var2.get(), width=5, textvariable=var6)
spin5.grid(column=0, row=8)
spin6.grid(column=1, row=8)
var5.trace_add('write', update_spinbox)
var6.trace_add('write', update_spinbox)
lbl6 = Label(window, text="Частота генерации:", font=("Calibri", 12))
lbl6.grid(column=0, row=9, pady=(20, 0))
var7 = DoubleVar()
var7.set(0.20)
spin7 = Spinbox(window, from_=0.05, to=0.45, increment=0.01, width=5,
                textvariable=var7)
spin7.grid(column=1, row=9, pady=(20, 0))
lbl8 = Label(window, text="(только для случайной)", font=("Calibri", 11))
lbl8.grid(column=0, row=10, columnspan=2)
lbl9 = Label(window, text="Алгоритм генерации:", font=("Calibri", 12))
lbl9.grid(column=2, row=0, padx=(70, 0))
generation = StringVar()
rad1 = Radiobutton(window, text="случайный", value="random",
                   variable=generation)
rad2 = Radiobutton(window, text='рекурсивный бэктрекер', value="recursive",
                   variable=generation)
rad3 = Radiobutton(window, text='алгоритм Прима', value="prim",
                   variable=generation)
rad1.grid(column=2, row=1)
rad2.grid(column=2, row=2, padx=(70, 0))
rad3.grid(column=2, row=3, padx=(32, 0))
lbl10 = Label(window, text="Алгоритм обхода:", font=("Calibri", 12))
lbl10.grid(column=2, row=4, padx=(70, 0), pady=(20, 0))
pathfinding = StringVar()
rad4 = Radiobutton(window, text="алгоритм Дейкстры", value="dijkstra",
                   variable=pathfinding)
rad5 = Radiobutton(window, text='алгоритм А*', value="a_star",
                   variable=pathfinding)
rad4.grid(column=2, row=5, padx=(45, 0))
rad5.grid(column=2, row=6, padx=(5, 0))
btn1 = Button(window, text="Создать с тонкими стенами", font=("Calibri", 11),
              width=25, activebackground="#fff7a3", background="#faebd7",
              command=clicked1)
btn2 = Button(window, text="Создать с объёмными стенами", font=("Calibri", 11),
              width=25, activebackground="#d3f7a3", background="#faebd7",
              command=clicked2)
btn1.grid(column=2, row=9, padx=(30, 0), pady=(20, 0))
btn2.grid(column=2, row=10, padx=(30, 0))
window.mainloop()
