from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font
from edit_inventary import open_inventary
from openpyxl import load_workbook
import openpyxl
import re
import sqlite3
import datetime

#=============DATA STRUCTURES DECLARATION=============
config = {}
products=[]
toSell=[]

#=====================CONSTANTS=======================
CONFIG_FILE="config.conf"

#=====================================================

def connectDataBase():
    conection = sqlite3.connect(config["DATA_BASE_NAME"])
    cursor = conection.cursor()
    try:
        cursor.execute(
            '''
            CREATE TABLE Inventario (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            PRODUCTO VARCHAN(100) NOT NULL,
            CANTIDAD INT NOT NULL)

            '''
        )
        conection.commit()
    except:
        conection.commit()
        cleanObject()
        show()
        messagebox.showinfo("CONECTADA","Se ha conectado a la base da datos.")
        
def products_update():
    products=[]
    conection = sqlite3.connect(config["DATA_BASE_NAME"])
    cursor = conection.cursor()
    cursor.execute("SELECT * FROM Inventario")
    for x in cursor:
        products.append(x[1])
    conection.commit()
    entry1=ttk.Combobox(main_windows,textvariable=name,values=products)
    entry1.place(relx=0.06, rely=0.1,relwidth=0.5,relheight=0.03)
    entry1.delete(0,"end")
    return products

def refresh():
    conection = sqlite3.connect(config["DATA_BASE_NAME"])
    cursor = conection.cursor()
    try:
        data=name.get(),value.get()
        cursor.execute("UPDATE Inventario SET PRODUCTO=?,CANTIDAD=? WHERE ID="+id.get(),(data))
        conection.commit()
    except:
        messagebox.showerror("ERROR","NO SE HA PODIDO ACTUALIZAR LA BASE DE DATOS")
        conection.commit()
        pass
    cleanObject()
    show()

def add():
    conection = sqlite3.connect(config["DATA_BASE_NAME"])
    cursor = conection.cursor()
    cursor.execute("SELECT * FROM Inventario")
    exit=0
    for x in cursor:
        if x[1]==name.get():
            try:
                quantity=int(x[2])+int(value.get())
                cursor.execute("UPDATE Inventario SET CANTIDAD={} WHERE PRODUCTO = '{}'".format(str(quantity),name.get()))
                conection.commit()
                exit=1
            except:
                messagebox.showerror("ERROR","NO SE HA PODIDO CONECTAR A BASE DE DATOS")
                exit=1
    if exit==0:
        try:
            data=name.get(),value.get()
            cursor.execute("INSERT INTO Inventario VALUES(NULL,?,?)",(data))
            conection.commit()
        except:
            messagebox.showerror("ERROR","NO SE HA PODIDO CONECTAR A BASE DE DATOS")
    
    cleanObject()
    show()

def show():
    conection = sqlite3.connect(config["DATA_BASE_NAME"])
    cursor = conection.cursor()
    logs = table.get_children()
    for x in logs:
        table.delete(x)
    try:
        cursor.execute("SELECT * FROM Inventario")
        for x in cursor:
            table.insert("",0,text=x[1],values=(x[2]))
        conection.commit()
    except:
        conection.commit()

def cleanObject():
    id.set("")
    name.set("")
    value.set("")

def exit():
    main_windows.destroy()
    
def addToSell():
    if entry1.get()!="" and entry_quantity.get()!="":
        toSell.append((entry1.get(),entry_quantity.get()))
        pre_sell_list.insert(0,entry1.get()+": "+entry_quantity.get())

def deleteToSell():
    for x in toSell:
        toSell.remove(x)
    pre_sell_list.delete(0,"end")

def sell():
    conection = sqlite3.connect(config["DATA_BASE_NAME"])
    cursor = conection.cursor()
    exit=0
    for x in toSell:
        cursor.execute("SELECT CANTIDAD FROM Inventario WHERE PRODUCTO='{}'".format(x[0]))
        if int(x[1])>cursor.fetchall()[0][0]:
            messagebox.showerror("ERROR","NO HAY STOCK SUFICENTE PARA '{}'".format(x[0]))
            exit=1
            break;
    if exit==1:
        for x in toSell:
            toSell.remove(x)
        pre_sell_list.delete(0,"end")
    else:
        for x in toSell:
            try:
                cursor.execute("SELECT CANTIDAD FROM Inventario WHERE PRODUCTO='{}'".format(x[0]))
                quantity=int(cursor.fetchall()[0][0])-int(x[1])
                cursor.execute("UPDATE Inventario SET CANTIDAD={} WHERE PRODUCTO = '{}'".format(str(quantity),x[0]))
                ws.append([datetime.datetime.now(), x[0], int(x[1])])
                wb.save(config["ROUTE_EXCEL"])
            except:
                messagebox.showerror("ERROR","NO SE HA PODIDO CONECTAR A LA BASE DE DATOS")
        for x in toSell:
            toSell.remove(x)
        pre_sell_list.delete(0,"end")
        conection.commit()
    cleanObject()
    show()

"""
That's function reads the file config.cof and charge his configurations
in the config dictionary, to use them.
"""
def loadConfig(file):
    regex = re.compile(r"(\w*) = \"(.*)\"") #Format: (name_conf) = (value)
    with open(file) as File:
        for x in regex.findall(File.read()):
            config[x[0]]=x[1]

loadConfig(CONFIG_FILE)

main_windows = Tk()
main_windows.geometry(config["SCREEN_SIZE_X"]+"x"+config["SCREEN_SIZE_Y"])
main_windows.title(config["NAME_ENTERPRISE"]+" - Inventario.")

wb = load_workbook(config["ROUTE_EXCEL"])
ws = wb.active

#Table creator

table=ttk.Treeview(heigh=15, columns=('#0'))
table.place(relx=0,rely=0.5,relwidth=1)
table.column('#0',width=720)
table.heading('#0',text="Productos", anchor=CENTER)
table.column('#1',width=100)
table.heading('#1',text="Cantidad", anchor=CENTER)


#=====================VARIABLES=======================

id=StringVar()
name=StringVar()
value=StringVar()

#=======================HUD===========================

startMenu=Menu(main_windows)
startMenuBD=Menu(startMenu, tearoff=0)

titleFont=Font(size=30)

lbl=Label(main_windows, text=config["NAME_ENTERPRISE"],font=titleFont)
lbl.pack()

lbl=Label(main_windows, text="Producto")
lbl.place(relx=0.01,rely=0.1,relwidth=0.05,relheight=0.03)


entry0=Entry(main_windows, textvariable=id)
products=products_update()

entry1=ttk.Combobox(main_windows,textvariable=name,values=products)

lbl=Label(main_windows, text="Cantidad")
lbl.place(relx=0.01,rely=0.15,relwidth=0.05,relheight=0.03)

lbl=Label(main_windows, text="Inventario")
lbl.place(relx=0.45,rely=0.47,relwidth=0.05,relheight=0.03)

entry_quantity=Entry(main_windows, textvariable=value)
entry_quantity.place(relx=0.06,rely=0.15)

add_sell_button=Button(main_windows, text="Agregar a Venta",command=addToSell)
add_sell_button.place(relx=0.16,rely=0.145)


pre_sell_list=Listbox(main_windows)
pre_sell_list.place(relx=0.01,rely=0.2,relwidth=0.5,relheight=0.25)

sell_button=Button(main_windows, text="Generar Venta",command=sell)
sell_button.place(relx=0.01,rely=0.452)

cancel_sell_button=Button(main_windows, text="Cancelar Venta",command=deleteToSell)
cancel_sell_button.place(relx=0.08,rely=0.452)

add_button=Button(main_windows, text="Editar a Inventario",command=open_inventary)
add_button.place(relx=0.155,rely=0.452)

btm_refresh=Button(main_windows,text="Actualizar",command=products_update)
btm_refresh.place(relx=0.24, rely=0.452)

connectDataBase()
main_windows.mainloop()