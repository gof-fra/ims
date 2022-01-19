from tkinter import*
from tkinter import font
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os
class saleClass:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1100x500+0+0")
        self.root.title("Système de gestion | developped by else.td")
        self.root.config(bg="white")
        self.root.focus_force()

        self.Bill_List=[]
        self.var_invoice=StringVar()

        #============Title===========
        lbl_title=Label(self.root, text="Les factures des clients", font=("goudy old style", 30), bg="#184a45", fg="white", bd=3, relief=RIDGE).pack(side=TOP, fill=X, padx=10, pady=20)

        lbl_invoice=Label(self.root, text="N° facture", font=("times new roman", 15), bg="black").place(x=50, y=100)

        txt_invoice=Entry(self.root, textvariable=self.var_invoice, font=("times new roman", 15), bg="#0f4d7d", fg="white").place(x=160, y=100, width=180, height=28)

        btn_search=Button(self.root, text="Chercher", command=self.search, font=("times new roman", 15), bg="#0f4d7d", fg="white" ).place(x=360, y=100, width=120, height=28)

        btn_clear=Button(self.root, text="Effacer", command=self.clear, font=("times new roman", 15), bg="#0f4d7d", fg="white" ).place(x=490, y=100, width=120, height=28)

        #=======Bill list=======
        sale_Frame=Frame(self.root, bd=3, relief=RIDGE)
        sale_Frame.place(x=50, y=140, width=200, height=330)

        scrolly=Scrollbar(sale_Frame, orient=VERTICAL)
        self.Sale_List=Listbox(sale_Frame, font=("goudy old style", 15), bg="#0f4d7d", fg="green", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.Sale_List.yview)
        self.Sale_List.pack(fill=BOTH, expand=1)
        self.Sale_List.bind("<ButtonRelease-1>", self.get_data)


        #=======Bill Area=======
        bill_Frame=Frame(self.root, bd=3, relief=RIDGE)
        bill_Frame.place(x=280, y=140, width=410, height=330)

        lbl_title2=Label(bill_Frame, text="Détails facture", font=("goudy old style", 20), bg="orange", fg="white", bd=3, relief=RIDGE).pack(side=TOP, fill=X)

        scrolly2=Scrollbar(bill_Frame, orient=VERTICAL)
        self.Bill_Area=Text(bill_Frame, bg='lightyellow', fg="black", yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.Bill_Area.yview)
        self.Bill_Area.pack(fill=BOTH, expand=1)
        

        #========Image========
        self.Bill_Photo=Image.open("images/1.png")
        self.Bill_Photo=self.Bill_Photo.resize((450, 300),Image.ANTIALIAS)
        self.Bill_Photo=ImageTk.PhotoImage(self.Bill_Photo)


        lbl_image=Label(self.root, image=self.Bill_Photo, bd=0)
        lbl_image.place(x=700, y=110)

        self.show()
        #===========================
    def show(self):
        del self.Bill_List[:]
        self.Sale_List.delete(0, END)
        #print(os.listdir('../IMS')) bill1.txt, category.py
        for i in os.listdir('bill'):
            #print(i.split('.'),i.split('.')[-1])
            if i.split('.')[-1]=='txt':
                self.Sale_List.insert(END,i)
                self.Bill_List.append(i.split('.')[0])

    
    def get_data(self, ev):
        index_=self.Sale_List.curselection()
        file_name=self.Sale_List.get(index_)
        #print(file_name)
        self.Bill_Area.delete('1.0', END)
        fp=open(f'bill/{file_name}', 'r')
        for i in fp:
            self.Bill_Area.insert(END,i)
        fp.close()

    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error", "Entrer le n° de facture!", parent=self.root)
        else:
            if self.var_invoice.get() in self.Bill_List:
                fp=open(f'bill/{self.var_invoice.get()}.txt', 'r')
                self.Bill_Area.delete('1.0', END)
                for i in fp:
                    self.Bill_Area.insert(END,i)
                fp.close()
            else:
                messagebox.showerror("Error", "Invalide n° de facuture!", parent=self.root)


    def clear(self):
        self.show()
        self.Bill_Area.delete('1.0', END)

if __name__=="__main__":
    root=Tk()
    obj=saleClass(root)
    root.mainloop()