from tkinter import *
import sqlite3
import csv
import re
import numpy as np
import matplotlib.pyplot as plt
'''
conn = sqlite3.connect('ffpm.db')
    c = conn.cursor()
    c.execute('INSERT INTO blessed("fecha", "lugar", "nom_H", "nom_M", "nac_H", "nac_M", "nacionalidad", "telefono") VALUES(fecha, lugar, nom_H, nom_M, nac_H, nac_M, nacionalidad, telefono)')

'''     
conn = sqlite3.connect('ffpm.db')
conn.text_factory = bytes
c = conn.cursor()


#Main Window
root = Tk()
#Size Main Window
root.geometry("600x600")
#Main Title
mainlabel = Label(root, text="Base de Datos FFPM"+"\n"+"Registro de Familias Bendecidas")
mainlabel.grid(row=0, column=0)

#SAVE DATA IN blessed TABLE
def save_data():
    #connecting to DB
    conn = sqlite3.connect('ffpm.db')
    #read DB as bytes
    conn.text_factory = bytes
    #create Cursor
    c = conn.cursor()
    #SQL command for FUNCTION
    c.execute('INSERT INTO blessed VALUES(NULL, :fecha, :lugar, :nom_H, :nom_M, :nac_H, :nac_M, :nacionalidad, :telefono)',
        {
            'fecha':fecha.get(),
            'lugar':lugar.get(),
            'nom_H':nom_H.get(),
            'nom_M':nom_M.get(),
            'nac_H':nac_H.get(),            
            'nac_M':nac_M.get(),
            'nacionalidad':nacionalidad.get(),
            'telefono':telefono.get()
                })
    #Commit Command
    conn.commit()
    #Close Connection
    conn.close()
    #Delete Labels AFTER Button

    fecha.delete(0, END)
    lugar.delete(0, END)
    nom_H.delete(0, END)
    nom_M.delete(0, END)
    nac_H.delete(0, END)
    nac_M.delete(0, END)
    nacionalidad.delete(0, END)
    telefono.delete(0, END)
    
#show REQUEST
def show_request():

    conn = sqlite3.connect('ffpm.db')
    conn.text_factory = bytes
    c = conn.cursor()
    c.execute('SELECT * FROM blessed WHERE lugar=?',(request,))
    conn.commit()

    conn.close()

    results.delete(0, END)
    return

#close search listbox
def close_search():
      list_search.destroy()

#show search listnox
def show():
    #connect to DB
    conn = sqlite3.connect('ffpm.db')
    #Change data text type to byte
    conn.text_factory = bytes
    #create cursor
    c = conn.cursor()
    #create schroll for listbox
    scroll = Scrollbar(root, orient=VERTICAL)
    #create close button
    close_button = Button(root, text="Cerrar", command=close_search)
    #declare global var
    global list_search
    #create listbox fro search results
    list_search = Listbox(root,width=600,yscrollcommand=scroll.set, highlightcolor="#ADD8E6")
    
    #get request entry
    entry = request_entry.get()
    #get dropmenu selction
    slct = clicked.get() 
    #actions if selection
    if slct == "fecha":
        c.execute("SELECT * FROM blessed WHERE fecha=?",(entry,))
    elif slct == "lugar":
            c.execute("SELECT * FROM blessed WHERE lugar=?",(entry,))
    elif slct == "Esposo":
            c.execute("SELECT * FROM blessed WHERE nom_H=?",(entry,))
    elif slct == "Esposa":
            c.execute("SELECT * FROM blessed WHERE nom_M=?",(entry,))
    elif slct == "Nacionalidad":
            c.execute("SELECT * FROM blessed WHERE nacionalidad=?",(entry,))
    elif slct == "Telefono":
            c.execute("SELECT * FROM blessed WHERE telefono=?",(entry,))
    #fetch selected data
    show = c.fetchall()
    #loop throuht data and insert into listbox
    for sh in show:
        list_search.insert(END, sh)
    #grid close listbox button
    close_button.grid(row=0, column=2)
    #config schroll bar
    scroll.config(command=list_search.yview)
    #grid schroll bar
    scroll.grid(sticky="n")
    #grid listbox
    list_search.grid(row=1, column=3, padx=10)
    #commit action in DB
    conn.commit()
    #close connection with DB
    conn.close()

#show all data
def show_ALL_data():
    conn = sqlite3.connect('ffpm.db')
    conn.text_factory = bytes
    c = conn.cursor()
    c.execute('SELECT * FROM blessed')
    data = c.fetchall()  
    #Create New Window
    top = Toplevel()
    top.title('Base de Datos FFPM')
    #Create Scrollbar
    scroll = Scrollbar(top, orient=VERTICAL)
    #delete button
    deletebutton = Button(top, text="Borrar", command=delete_record)
    deletebutton.pack()

    #Create Listbox
    global top_bx
    top_bx = Listbox(top, width=800, height=800, yscrollcommand=scroll.set, highlightcolor="#ADD8E6")
    #loop thru results
    for dats in data:
        top_bx.insert(END, dats)
    #Config scrollbar into label
    scroll.config(command=top_bx.yview)
    scroll.pack(side=RIGHT, fill=Y)
    top_bx.pack()
    conn.commit()
    #regx =  re.compile(r'[^\sb]')
#find = regx.findall(str(dats))

#graph_progress function
def graph_progress():
    conn = sqlite3.connect('ffpm.db')
    conn.text_factory = bytes
    c = conn.cursor()
    c.execute("SELECT * FROM blessed")
    dt = c.fetchall()
    flias = len(dt)
    plt.hist(430, flias)
    plt.show()
    
    print(flias)    

    conn.commit()
    conn.close()
#delete 
def delete_record():
    conn = sqlite3.connect('ffpm.db')
    conn.text_factory = bytes
    c = conn.cursor()
    #GET selected item from listbox
    select_line =  top_bx.get(ACTIVE)
    #display ID from selected item
    select_line = select_line[0]
    #delete row from table in DB
    c.execute("DELETE FROM blessed WHERE oid=?",(select_line,))
    #delete item from listbox
    top_bx.delete(ANCHOR)
    conn.commit()
    conn.close()


    ''' def del_notes():
                    # get selected person       
                    person = content.get(ACTIVE)
                    name = person[0]
            
                    # delete in database
                    c = self.conn.cursor()
                    c.execute("DELETE FROM people WHERE name=?", (name))
                    self.conn.commit()
                    c.close()
            
                    # delete on list
                    self.content.delete(ANCHOR)'''
############################################################################### AQUI TERMINASTE!!!!  ###############################################################################


#Create Labels
titlelabel = Label(root, text="Ingrese los datos requeridos")
#Grid Labels
titlelabel.grid(row=1, column=0)

fecha_l = Label(root, text="Fecha:")
fecha_l.grid(row=2, column=0)
fecha = Entry(root, text="Fecha", width=30,)
fecha.grid(row=2, column=1)

lugar_l = Label(root, text="Lugar:")
lugar_l.grid(row=3, column=0)
lugar = Entry(root, text="Lugar", width=30,)
lugar.grid(row=3, column=1)

nom_H_l = Label(root, text="Nombre del Esposo:")
nom_H_l.grid(row=4, column=0)
nom_H = Entry(root, text="Nombre del Esposo", width=30,)
nom_H.grid(row=4, column=1)

nom_M_l = Label(root, text="Nombre de la Esposa:")
nom_M_l.grid(row=5, column=0)
nom_M = Entry(root, text="Nombre de la Esposa", width=30,)
nom_M.grid(row=5, column=1)

nac_H_l = Label(root, text="Nacimiento(esposo):")
nac_H_l.grid(row=6, column=0)
nac_H = Entry(root, text="Nacimiento: DD/MM/AAAA esposo", width=30,)
nac_H.grid(row=6, column=1)

nac_M_l= Label(root, text="Nacimiento(esposa):")
nac_M_l.grid(row=7, column=0)
nac_M = Entry(root, text="Nacimiento: DD/MM/AAAA esposa", width=30,)
nac_M.grid(row=7, column=1)

nacionalidad_l = Label(root, text="Nacionalidad:")
nacionalidad_l.grid(row=8, column=0)
nacionalidad = Entry(root, text="Nacionalidad", width=30,)
nacionalidad.grid(row=8, column=1)

telefono_l = Label(root, text="Telefono o Email")
telefono_l.grid(row=9, column=0)
telefono = Entry(root, text="Telefono o Email", width=30,)
telefono.grid(row=9, column=1)


#insert data
srcbutton = Button(root, text="Guardar", command=save_data)
srcbutton.grid(row=10, column=0)




clicked = StringVar()
clicked.set("opciones de busqueda")

request_l = Label(root, text="Buscar datos en los registros:")
request_l.grid(row=15, column=0, pady=5)
request = OptionMenu(root, clicked,"fecha", "lugar", "Esposo","Esposa", "Nacionalidad", "Telefono")
request.grid(row=16, column=0, pady=5)
request_entry = Entry(root, width=30,)
request_entry.grid(row=16, column=1)
 
#search request button
search = Button(root, text="buscar", command=show)
search.grid(row=16, column=2, pady=10, padx=10)

#search all button
srcbutton = Button(root, text="Mostrar todo el registro", command=show_ALL_data)
srcbutton.grid(row=17, column=0, pady=10, padx=10)


graph_button = Button(root, text="graficar progreso", command=graph_progress)
graph_button.grid(row=18, column=0, pady=10, padx=10)


'''
results = Label(root, text=dts)
results.grid(row=11, column=0)
'''



conn.commit()

conn.close()

root.mainloop()