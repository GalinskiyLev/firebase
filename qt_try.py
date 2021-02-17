from tkinter import *
from tkinter import scrolledtext 
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd 
from tkinter.ttk import Combobox
import csv


# initialize sdk
cred = credentials.Certificate("project-8c564-firebase-adminsdk-66h2w-4c95489651.json")
#firebase_admin.initialize_app(cred)
db = firestore.client()

def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        #print(f'Deleting doc {doc.id} => {doc.to_dict()}')
        doc.reference.delete()
        deleted = deleted + 1
    
    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)






cf=db.collection(u'playlist')
delete_collection(cf, 1)


df = pd.read_csv('mashka_input.csv')
#df_pd = 
def writeONscreen(): 
    txt.delete(1.0, END)
    txt.insert(INSERT,df)  
def write_on_screen_bd(): 
    screen_bd.delete(1.0, END)
    screen_bd.insert(INSERT,db)  
def TO_FB():
    txt.delete(1.0, END)
    for i in range(len(df)): 
        doc_ref = db.collection(u'playlist').document()
        doc_ref.set({
            df.columns[0]: df.loc[i,df.columns[0]],
            df.columns[1]: df.loc[i,df.columns[1]],
            df.columns[2]: df.loc[i,df.columns[2]],
                })
    txt.insert(INSERT,"Данные отправлены")

def fromFBtoLocalCSV():
    txt.delete(1.0, END)
    with open('mashka_output.csv', 'w', newline='') as csvfile:
        fieldnames = [df.columns[0], df.columns[1], df.columns[2]]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        docs = list(db.collection(u'playlist').get())
        for doc in docs:
            writer.writerow(doc.to_dict())
    txt.insert(INSERT,"Данные экспортированы на Ваш компьютер в формате CSV(lol_output.csv)")

    #https://code.tutsplus.com/ru/tutorials/how-to-read-and-write-csv-files-in-python--cms-29907





root = Tk()
root.title("Что-то там со списками")
root.geometry('1400x900')

txt = scrolledtext.ScrolledText(root, width=30, height=20)  
txt.grid(column=0, row=0) 

screen_bd = scrolledtext.ScrolledText(root, width=30, height=20)
screen_bd.place(x = 1000, y = 0, width = 400, height = 800)
write_on_screen_bd()
btn = Button(root, text="Вывести локальный документ", command=writeONscreen)
btn.grid(column=1, row=0)

btn1 = Button(root, text="Экспортировать в CSV из FIREBASE", command=fromFBtoLocalCSV)
btn1.grid(column=1, row=1)
btn2 = Button(root, text="Отправить данные CSV в FIREBASE", command=TO_FB)
btn2.grid(column=0, row=1)
btn3 = Button(root, text="Show Vac", command=show)
btn3.grid(column=2, row=1)

#cols = db.collections()
#list_col = []
#for col in cols:
     #list_col.append(col.id)
#print(list_col)
def show():
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
    
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')  


def display_full_name():
    b=cf.loc[1,df.columns[1]]
    messagebox.showinfo("GUI Python", name.get() + " " + surname.get()+b)
    
 
name = StringVar()
surname = StringVar()
 
name_label = Label(text="Введите имя:")
surname_label = Label(text="Введите фамилию:")
 
name_label.grid(row=0, column=3, sticky="w")
surname_label.grid(row=1, column=3, sticky="w")
 
name_entry = Entry(textvariable=name)
surname_entry = Entry(textvariable=surname)
 
name_entry.grid(row=0,column=4, padx=5, pady=5)
surname_entry.grid(row=1,column=4, padx=5, pady=5)
 
 
message_button = Button(text="Click Me", command=display_full_name)
message_button.grid(row=3,column=4, padx=5, pady=5, sticky="e")

root.mainloop()









