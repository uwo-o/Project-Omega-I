from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font
from typing import Collection
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

def update_table():
    conection=sqlite3.connect(config["DATA_BASE_NAME"])
    cursor=conection.cursor()
    cursor.execute("SELECT * FROM Inventario")
    conection.commit()
    logs = mini_table.get_children()
    for x in logs:
        mini_table.delete(x)
    for x in cursor:
        mini_table.insert("",0,text=x[0],values=(x[1],x[2]))

def add_product():
    conection=sqlite3.connect(config["DATA_BASE_NAME"])
    cursor=conection.cursor()
    try:
        if product.get()!="" and quantity.get()!="":
            cursor.execute("INSERT INTO Inventario VALUES(NULL,'{}','{}')".format(product.get(),quantity.get()))
            conection.commit()
            update_table()
            product_entry.delete(0,"end")
            quantity_entry.delete(0,"end")

        else:
            messagebox.showinfo("ADVERTENCIA","LOS CAMPOS NO PUEDEN ESTAR VACIOS")
    except:
        pass

def delete_product():
    conection=sqlite3.connect(config["DATA_BASE_NAME"])
    cursor=conection.cursor()
    try:
        if id2_entry.get()!="":
            cursor.execute("DELETE FROM Inventario WHERE ID='{}'".format(id2_entry.get()))
            conection.commit()
            update_table()
            id2_entry.delete(0,"end")
        else:
            messagebox.showinfo("ADVERTENCIA","LOS CAMPOS NO PUEDEN ESTAR VACÍOS")

    except:
        pass

def update_stock():
    conection=sqlite3.connect(config["DATA_BASE_NAME"])
    cursor=conection.cursor()
    try:
        if id_entry.get()!="" and quantity_entry2.get()!="":
            cursor.execute("UPDATE Inventario SET CANTIDAD={} WHERE ID = '{}'".format(quantity_entry2.get(),id_entry.get()))
            conection.commit()
            update_table()
            id_entry.delete(0,"end")
            quantity_entry2.delete(0,"end")
        else:
            messagebox.showinfo("ADVERTENCIA","LOS CAMPOS NO PUEDEN ESTAR VACÍOS")
    
    except:
        pass

def set_frame3():
    frame3.place(x=670,y=50,relheight=0.42,relwidth=0.465)
    edit_button['state'] = DISABLED
    cancel_edit_button['state'] = NORMAL

def destroy_frame3(value):
    quantity_entry.delete(0,"end")
    product_entry.delete(0,"end")
    frame3.place(x=-670,y=-50,relheight=0.4,relwidth=0.465)
    cancel_edit_button['state'] = DISABLED
    edit_button['state'] = NORMAL
    if value==1:
        products_update()

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
    entry1=ttk.Combobox(frame1,textvariable=name,values=products,width=40)
    entry1.grid(row=1,column=0,columnspan=3)
    entry1.delete(0,"end")
    show()
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
        flag=0
        for x in toSell:
            if x[0]==entry1.get():
                flag=1
        if flag==1:
            aux=int(x[1])
            aux+=int(entry_quantity.get())
            x[1]=str(aux)
            pre_sell_list.delete(0,"end")
            pre_sell_list.insert(0,x[0]+": "+x[1])     
        else:    
            toSell.append([entry1.get(),entry_quantity.get()])
            pre_sell_list.insert(0,entry1.get()+": "+entry_quantity.get())

def deleteToSell():
    for x in toSell:
        toSell.pop()
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
main_windows.resizable(width=0, height=0)

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
connectDataBase()
startMenu=Menu(main_windows)
startMenuBD=Menu(startMenu, tearoff=0)

titleFont=Font(size=30)

frame1=Frame(main_windows)
frame1.place(x=10,y=50,relheight=0.4,relwidth=0.5)
frame2=Frame(main_windows)
frame2.place(x=540,y=110,relheight=0.3,relwidth=0.1)
frame3=Frame(main_windows)


lbl=Label(main_windows, text=config["NAME_ENTERPRISE"],font=titleFont)
lbl.pack()

#================
#Frame 1 widgets
#================

entry1=ttk.Combobox(frame1,textvariable=name,values=products,width=40)
entry1.grid(row=1,column=0,columnspan=3)

lbl=Label(frame1, text="Producto")
lbl.grid(row=0,column=1)

entry0=Entry(frame1, textvariable=id)

products=products_update()

lbl=Label(frame1, text="Cantidad")
lbl.grid(row=0,column=4)

entry_quantity=Entry(frame1, textvariable=value)
entry_quantity.grid(row=1,column=3,padx=10,columnspan=3)

add_sell_button=Button(frame1, text="Agregar a Venta",command=addToSell)
add_sell_button.grid(row=1,column=7)


pre_sell_list=Listbox(frame1,height=50,width=85)
pre_sell_list.grid(row=2,column=0,pady=10,columnspan=8)

#=================
#Frame 2 widgets
#=================

btm_refresh=Button(frame2,text="Actualizar",command=products_update,width=15)
btm_refresh.grid(row=0,pady=1)

edit_button=Button(frame2, text="Editar Inventario",command=set_frame3,width=15)
edit_button.grid(row=1,pady=1)

cancel_edit_button=Button(frame2, text="Cerrar Inventario",command=lambda:destroy_frame3(value=0),width=15)
cancel_edit_button.grid(row=2,pady=1)
cancel_edit_button['state'] = DISABLED

cancel_sell_button=Button(frame2, text="Cancelar Venta",command=deleteToSell,width=15)
cancel_sell_button.grid(row=3,pady=1)

sell_button=Button(frame2, text="Generar Venta",command=sell,width=15)
sell_button.grid(row=4,pady=1)

#================
#Frame 3 widgets
#================

product=StringVar()
quantity=StringVar()
id=StringVar()
id2=StringVar()
quantity2=StringVar()

edit_quiantity=StringVar()
edit_id=StringVar()

delete_id=StringVar()

Label(frame3,text="INVENTARIO").grid(padx=5,pady=5,row=0,column=0,columnspan=4)


mini_table=ttk.Treeview(frame3,heigh=5, columns=('#0','#1'))
mini_table.grid(row=1,column=0,rowspan=4,columnspan=9)
mini_table.column('#0',width=50)
mini_table.heading('#0',text="ID", anchor=CENTER)
mini_table.column('#1',width=280)
mini_table.heading('#1',text="Productos", anchor=CENTER)
mini_table.column('#2',width=75)
mini_table.heading('#2',text="Cantidad", anchor=CENTER)


Label(frame3,text="INGRESAR PRODUCTO").grid(row=8,column=0)
Label(frame3,text="PRODUCTO").grid(padx=10,row=7, column=1)
Label(frame3,text="CANTIDAD").grid(row=7, column=3)

product_entry=Entry(frame3,width=50,textvariable=product)
product_entry.grid(padx=10,row=8, column=1,columnspan=3)

quantity_entry=Entry(frame3,width=10,textvariable=quantity)
quantity_entry.grid(row=8, column=3,columnspan=1)

Button(frame3,text="INGRESAR",command=lambda:add_product()).grid(padx=10,row=8,column=4)

Label(frame3,text="EDITAR STOCK").grid(row=10,column=0)
Label(frame3,text="ID").grid(row=9,column=1)
Label(frame3,text="CANTIDAD").grid(row=9,column=3)

id_entry=Entry(frame3,width=10,textvariable=edit_id)
id_entry.grid(row=10,column=1)

quantity_entry2=Entry(frame3,width=20,textvariable=edit_quiantity)
quantity_entry2.grid(row=10,column=3)

Button(frame3,text="ACTUALIZAR",command=lambda:update_stock()).grid(row=10,column=4)

Label(frame3,text="ELIMINAR").grid(row=12,column=0)
Label(frame3,text="ID").grid(row=11,column=1)

id2_entry=Entry(frame3,width=10,textvariable=delete_id)
id2_entry.grid(row=12,column=1)

Button(frame3,text="ELIMINAR",command=lambda:delete_product()).grid(row=12,column=4)

update_table()



#=================
#main_windows widgets
#=================

lbl=Label(main_windows, text="Inventario")
lbl.place(relx=0.45,rely=0.47,relwidth=0.05,relheight=0.03)


main_windows.mainloop()