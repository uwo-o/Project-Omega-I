from tkinter import *
from tkinter import ttk
from typing import List
from tkinter import messagebox

import sqlite3


def select(etr,list):
    etr.delete(0,"end")
    etr.insert(0,list.get(ANCHOR))

def add(root,etr,list,products,config):
    conection = sqlite3.connect(config["DATA_BASE_NAME"])
    cursor = conection.cursor()
    if etr.get() not in products:
        try:
            cursor.execute("INSERT INTO Productos(ID,PRODUCTO) VALUES(NULL,'{}')".format(etr.get()))
            conection.commit()
            products.append(etr.get())
            root.destroy()
        except:
            messagebox.showerror("ERROR", "No se ha podido actualizar la base de datos.")
            root.destroy()
    else:
        messagebox.showinfo("EROOR","EL VALOR INGRESADO YA EXISTE") 

def delete(root,etr,list,products,config):
    conection = sqlite3.connect(config["DATA_BASE_NAME"])
    cursor = conection.cursor()
    if etr.get() in products:
        try:
            cursor.execute("DELETE FROM Productos WHERE PRODUCTO='{}'".format(etr.get()))
            conection.commit()
            products.remove(etr.get())
            root.destroy()
        except Exception as E:
            messagebox.showerror("ERROR", E)
            root.destroy()
    else:
        messagebox.showinfo("EROOR","NO EXISTE EL PRODUCTO") 


def open_inventary(products,config):
    root=Tk()
    root.title("Productos")
    root.geometry("400x400")

    producto_name=StringVar()

    lbl=Label(root,text="Productos").pack()
 
    list=Listbox(root)
    for x,y in enumerate(products):
        list.insert(x+1,y)
    list.pack(fill="x")
    
    etr=Entry(root,textvariable=producto_name)
    btn=Button(root, text="Seleccionar", command=lambda:select(etr,list))

    btn.pack(pady=10)
    etr.pack(fill="x")

    btn1=Button(root, text="Agregar", command=lambda:add(root,etr,list,products,config)).pack(pady=10)
    
    btn_delete=Button(root, text="Borrar", command=lambda:delete(root,etr,list,products,config)).pack(pady=10)

    root.mainloop()

