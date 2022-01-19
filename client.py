from tkinter import*
from tkinter import font
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
class clientClass:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1100x500+0+0")
        self.root.title("Système de gestion | developped by else.td")
        self.root.config(bg="white")
        self.root.focus_force()

        #================================
        #===========All Variables =======
        self.var_searchBy=StringVar()
        self.var_searchTxt=StringVar()

        self.var_cli_invoice=StringVar()
        self.var_cli_nom=StringVar()
        self.var_cli_contact=StringVar()

        #=======search=======
        #=======option=====
        lbl_search=Label(self.root, text="Facture n°", bg="gray", font=("goudy old style", 15))
        lbl_search.place(x=700,y=80)
        
        txt_search=Entry(self.root, textvariable=self.var_searchTxt, font=("goudy old style", 15), bg="gray").place(x=800, y=80, width=160)
        btn_search=Button(self.root, text="Chercher", command=self.search, font=("goudy old style", 15), bg="green", fg="black").place(x=980,y=79, width=100, height=28)

        #======Title====
        title=Label(self.root, text="Informations clients",font=("goudy old style", 20, "bold"),
        bg="#0f4d7d", fg="white").place(x=50,y=10,width=1000, height=40)

        #====content======
        #====row1=======
        lbl_cli_invoice=Label(self.root, text="Facure no°", font=("goudy old style", 15), bg="white", fg="black").place(x=50,y=80)
         
        txt_cli_invoice=Entry(self.root, textvariable=self.var_cli_invoice, font=("goudy old style", 15), bg="lightyellow", fg="black").place(x=180,y=80, width=180)
        

        #====row2=======
        lbl_nom=Label(self.root, text="Nom:", font=("goudy old style", 15), bg="white", fg="black").place(x=50,y=160)
        
        txt_nom=Entry(self.root, textvariable=self.var_cli_nom, font=("goudy old style", 15), bg="lightyellow", fg="black").place(x=180,y=160, width=180)
        
        
        #====row3=======
        lbl_contact=Label(self.root, text="Contact:", font=("goudy old style", 15), bg="white", fg="black").place(x=50,y=120)
         
        txt_contact=Entry(self.root, textvariable=self.var_cli_contact, font=("goudy old style", 15), bg="lightyellow", fg="black").place(x=180,y=120, width=180)
       

        #====row4=======
        lbl_desc=Label(self.root, text="Description:", font=("goudy old style", 15), bg="white", fg="black").place(x=50,y=200)
        
        self.txt_desc=Text(self.root, font=("goudy old style", 15), bg="lightyellow", fg="black")
        self.txt_desc.place(x=180,y=200, width=470, height=120)
        

        #=====Buttons======
        btn_add=Button(self.root, text="Ajouter", command=self.add, font=("goudy old style", 15),  
        fg="black", bg="#00FA9A", cursor="hand2").place(x=180,y=370, width=110, height=35)
        btn_update=Button(self.root, text="Mis-a-jour", command=self.update, font=("goudy old style", 15), 
        fg="black", bg="#00FA9A", cursor="hand2").place(x=300,y=370, width=110, height=35)
        btn_delete=Button(self.root, text="Supprimer", command=self.delete, font=("goudy old style", 15), 
        fg="black", bg="#00FA9A", cursor="hand2").place(x=420,y=370, width=110, height=35)
        btn_clear=Button(self.root, text="Effacer", command=self.clear, font=("goudy old style", 15), 
        fg="black", bg="#00FA9A", cursor="hand2").place(x=540,y=370, width=110, height=35)


        #=======Employees Details======
        emp_frame=Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=700, y=120, width=380, height=350)

        scolly=Scrollbar(emp_frame, orient=VERTICAL)
        scollx=Scrollbar(emp_frame, orient=HORIZONTAL)

        self.ClientTable=ttk.Treeview(emp_frame, columns=("invoice", "nom", "contact", "desc"), 
        yscrollcommand=scolly.set, xscrollcommand=scollx.set)
        
        scollx.pack(side=BOTTOM, fill=X)
        scolly.pack(side=RIGHT, fill=Y)
        scollx.config(command=self.ClientTable.xview)
        scolly.config(command=self.ClientTable.yview)

        self.ClientTable.heading("invoice", text="Facture n°.")
        self.ClientTable.heading("nom", text="Nom")
        self.ClientTable.heading("contact", text="Contact")
        self.ClientTable.heading("desc", text="Desc")
        

        self.ClientTable["show"]="headings"

        self.ClientTable.column("invoice", width=90)
        self.ClientTable.column("nom", width=100)
        self.ClientTable.column("contact", width=100)
        self.ClientTable.column("desc", width=100)
        
        self.ClientTable.pack(fill=BOTH, expand=1)
        self.ClientTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

#================   ==  =   =   =   =   =   =   ============
    #========ADD===============================
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()

        try:
            if self.var_cli_invoice.get()=="":
                messagebox.showerror("Error", "Entrer n° facture", parent=self.root)
            else:
                cur.execute("Select * from client where invoice=?", (self.var_cli_invoice.get(), ))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error", "N° pris, essayez different", parent=self.root)
                else:
                    cur.execute("Insert into client (invoice, nom, contact, desc) values(?,?,?,?)",(
                                        self.var_cli_invoice.get(),
                                        self.var_cli_nom.get(),
                                        
                                        self.var_cli_contact.get(),

                                        self.txt_desc.get('1.0', END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Success!", parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        #=======END ADD===========


    #========UPDATE===============================
    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()

        try:
            if self.var_cli_invoice.get()=="":
                messagebox.showerror("Error", "Entrer n° facture!", parent=self.root)
            else:
                cur.execute("Select * from client where invoice=?", (self.var_cli_invoice.get(), ))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Invalid invoice n°.", parent=self.root)
                else:
                    cur.execute("Update client set nom=?, contact=?, desc=? where invoice=?",(
                                        self.var_cli_nom.get(),
                                        self.var_cli_contact.get(),

                                        self.txt_desc.get('1.0', END),

                                        self.var_cli_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Succes!", parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        #=======END UPDATE===========

    #========DELETE===============================
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()

        try:
            if self.var_cli_invoice.get()=="":
                messagebox.showerror("Error", "Entrer n° facture!", parent=self.root)
            else:
                cur.execute("Select * from client where invoice=?", (self.var_cli_invoice.get(), ))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Invalid invoice n°", parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm", "Supprimer?", parent=self.root)
                    if op==True:
                        cur.execute("delete from client where invoice=?", (self.var_cli_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Client deleted sucessfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        #=======END DELETE===========

    #========CLEAR===============================
    def clear(self):
        self.var_cli_invoice.set(""),
        self.var_cli_nom.set(""),
        self.var_cli_contact.set(""),
        self.txt_desc.delete('1.0', END),
        self.var_searchTxt.set(""),
        self.var_searchBy.set("Select")
        self.show()   
    #=======END CLEAR===========

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchTxt.get()=="":
                messagebox.showerror("Error", "Entrer n° facture!", parent=self.root)
            else:  
                cur.execute("Select * from client where invoice=?", (self.var_searchTxt.get(),))
                row=cur.fetchone()
                if row!=0:
                    self.ClientTable.delete(*self.ClientTable.get_children())
                    self.ClientTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "Sans succes!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

        

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from client")
            rows=cur.fetchall()
            self.ClientTable.delete(*self.ClientTable.get_children())
            for row in rows:
                self.ClientTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)



    #====get data on click to update
    def get_data(self, ev):
        f=self.ClientTable.focus()
        content=(self.ClientTable.item(f))
        row=content['values']
        #print(row)
        self.var_cli_invoice.set(row[0]),
        self.var_cli_nom.set(row[1]),
        self.var_cli_contact.set(row[2]),
        self.txt_desc.delete('1.0', END),
        self.txt_desc.insert(END, row[3]),
   
if __name__=="__main__":
    root=Tk()
    obj=clientClass(root)
    root.mainloop()