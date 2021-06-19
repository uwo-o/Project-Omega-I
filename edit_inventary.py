from re import T
from tkinter import *
from tkinter import ttk
from typing import List
from tkinter import messagebox
import sqlite3


def update_table(config,table):
    conection=sqlite3.connect(config["DATA_BASE_NAME"])
    cursor=conection.cursor()
    cursor.execute("SELECT * FROM Inventario")
    conection.commit()
    logs = table.get_children()
    for x in logs:
        table.delete(x)
    for x in cursor:
        table.insert("",0,text=x[0],values=(x[1],x[2]))

def add_product(config,table,product,quantity):
    conection=sqlite3.connect(config["DATA_BASE_NAME"])
    cursor=conection.cursor()
    try:
        if product.get()!="" and quantity.get()!="":
            cursor.execute("INSERT INTO Inventario VALUES(NULL,'{}','{}')".format(product.get(),quantity.get()))
            conection.commit()
            update_table(config,table)
            product.delete(0,"end")
            quantity.delete(0,"end")

        else:
            messagebox.showinfo("ADVERTENCIA","LOS CAMPOS NO PUEDEN ESTAR VACIOS")
    except:
        pass

def delete_product(config,table,id_entry):
    conection=sqlite3.connect(config["DATA_BASE_NAME"])
    cursor=conection.cursor()
    try:
        if id_entry.get()!="":
            cursor.execute("DELETE FROM Inventario WHERE ID='{}'".format(id_entry.get()))
            conection.commit()
            update_table(config,table)
            id_entry.delete(0,"end")
        else:
            messagebox.showinfo("ADVERTENCIA","LOS CAMPOS NO PUEDEN ESTAR VACÍOS")

    except:
        pass

def update_stock(config,table,id_entry2,quantity_entry2):
    conection=sqlite3.connect(config["DATA_BASE_NAME"])
    cursor=conection.cursor()
    try:
        if id_entry2.get()!="" and quantity_entry2.get()!="":
            cursor.execute("UPDATE Inventario SET CANTIDAD={} WHERE ID = '{}'".format(quantity_entry2.get(),id_entry2.get()))
            conection.commit()
            update_table(config,table)
            id_entry2.delete(0,"end")
            quantity_entry2.delete(0,"end")
        else:
            messagebox.showinfo("ADVERTENCIA","LOS CAMPOS NO PUEDEN ESTAR VACÍOS")
    
    except:
        pass

def open_inventary(config):

    root=Tk()
    root.title("Editar Inventario")
    root.geometry("400x600")
    root.resizable(width=0, height=0)

    product=StringVar()
    quantity=StringVar()
    id=StringVar()
    id2=StringVar()
    quantity2=StringVar()
    Label(root,text="PRODUCTO").grid(padx=10,row=0, column=0)
    Label(root,text="CANTIDAD").grid(row=0, column=2)

    product_entry=Entry(root,width=50,textvariable=product)
    product_entry.grid(padx=10,row=1, column=0)
    quantity_entry=Entry(root,width=10,textvariable=quantity)
    quantity_entry.grid(row=1, column=2)

    Button(root,width=40,text="INGRESAR",command=lambda:add_product(config,table,product_entry,quantity_entry)).grid(padx=5,pady=5,row=2,column=0,columnspan=3)

    Label(root,text="INVENTARIO").grid(padx=5,pady=5,row=3,column=0,columnspan=3)

    
    table=ttk.Treeview(root,heigh=15, columns=('#0','#1'))
    table.place(x=10,y=100)
    table.column('#0',width=50)
    table.heading('#0',text="ID", anchor=CENTER)
    table.column('#1',width=250)
    table.heading('#1',text="Productos", anchor=CENTER)
    table.column('#2',width=75)
    table.heading('#2',text="Cantidad", anchor=CENTER)

    Label(root,text="ELIMINAR").place(x=160,y=430)
    Label(root,text="ID").place(x=5,y=455)
    id_entry=Entry(root,width=25,textvariable=id)
    id_entry.place(x=30,y=455)

    Button(root,text="ACEPTAR",command=lambda:delete_product(config,table,id_entry)).place(x=200,y=450)

    Label(root,text="ACTUALIZAR STOCK").place(x=140,y=480)
    Label(root,text="ID").place(x=5,y=505)
    id_entry2=Entry(root,width=25,textvariable=id2)
    id_entry2.place(x=30,y=505)
    Label(root,text="CANTIDAD").place(x=5,y=535)
    quantity_entry2=Entry(root,width=18,textvariable=quantity2)
    quantity_entry2.place(x=70,y=535)

    Button(root,text="ACEPTAR",command=lambda:update_stock(config,table,id_entry2,quantity_entry2)).place(x=200,y=520)
    

    update_table(config,table)

    root.mainloop()



