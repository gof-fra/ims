from tkinter import*
from tkinter import font
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
class employeeClass:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1100x500+0+0")
        self.root.title("Système de gestion | developped by else.td")
        self.root.config(bg="white")
        self.root.focus_force()

        #============================
        #===========All Variables =======
        self.var_searchBy=StringVar()
        self.var_searchTxt=StringVar()

        self.var_emp_id=StringVar()
        self.var_emp_nom=StringVar()
        self.var_emp_contact=StringVar()
        self.var_emp_sexe=StringVar()
        self.var_emp_dateDebut=StringVar()
        self.var_emp_dateFin=StringVar()
        self.var_emp_email=StringVar()
        self.var_emp_password=StringVar()
        self.var_emp_uType=StringVar()
        self.var_emp_salaire=StringVar()
        self.var_emp_address=StringVar()

        #=======search=======
        SearchFrame=LabelFrame(self.root,text="Rechercher employés",font=("goudy old style", 12, 
        "bold"), bd=2, relief=RIDGE, bg="green")
        SearchFrame.place(x=250,y=20,width=600,height=70)


        #=======option=====
        cmb_search=ttk.Combobox(SearchFrame, textvariable=self.var_searchBy, values=("Select", "Nom", 
        "Email", "Contact"), state='readonly', justify=CENTER, font=("goudy old style", 15), )
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame, textvariable=self.var_searchTxt, font=("goudy old style", 15), bg="gray").place(x=200, y=10)
        btn_search=Button(SearchFrame, text="Chercher", command=self.search, font=("goudy old style", 15), bg="gray", fg="white").place(x=410,y=10, width=150, height=30)

        #======Title====
        title=Label(self.root, text="Informations employés",font=("goudy old style", 15),
        bg="#0f4d7d", fg="white").place(x=50,y=100,width=1000)

        #====content======
        #====row1=======
        lbl_empId=Label(self.root, text="Emp. ID:", font=("goudy old style", 15), bg="white", fg="black").place(x=50,y=150)
        lbl_sexe=Label(self.root, text="Type:", font=("goudy old style", 15), bg="white", fg="black").place(x=350,y=150)
        lbl_contact=Label(self.root, text="Contact:", font=("goudy old style", 15), bg="white", fg="black").place(x=750,y=150)
         
        txt_empId=Entry(self.root, textvariable=self.var_emp_id, font=("goudy old style", 15), bg="lightyellow", fg="black").place(x=150,y=150, width=180)
        cmb_sexe=ttk.Combobox(self.root, textvariable=self.var_emp_sexe, values=("Homme", 
        "Femme"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_sexe.place(x=500,y=150,width=180)
        cmb_sexe.current(0)
        txt_contact=Entry(self.root, textvariable=self.var_emp_contact, font=("goudy old style", 15), bg="lightyellow", fg="black").place(x=850,y=150, width=180)
         

        #====row2=======
        lbl_nom=Label(self.root, text="Nom:", font=("goudy old style", 15), bg="white", fg="black").place(x=50,y=190)
        lbl_dateDebut=Label(self.root, text="Date debut:", font=("goudy old style", 15), bg="white", fg="black").place(x=350,y=190)
        lbl_dateFin=Label(self.root, text="Date fin:", font=("goudy old style", 15), bg="white", fg="black").place(x=750,y=190)
         
        txt_nom=Entry(self.root, textvariable=self.var_emp_nom, font=("goudy old style", 15), bg="lightyellow", fg="black").place(x=150,y=190, width=180)
        txt_dateDebut=Entry(self.root, textvariable=self.var_emp_dateDebut, font=("goudy old style", 15), bg="lightyellow", fg="black").place(x=500,y=190, width=180)
        txt_dateFin=Entry(self.root, textvariable=self.var_emp_dateFin, font=("goudy old style", 15), bg="lightyellow", fg="black").place(x=850,y=190, width=180)
         
        
        #====row3=======
        lbl_email=Label(self.root, text="Email:", font=("goudy old style", 15), bg="white", fg="black").place(x=50,y=230)
        lbl_password=Label(self.root, text="Password:", font=("goudy old style", 15), bg="white", fg="black").place(x=350,y=230)
        lbl_Type=Label(self.root, text="Utilisateur:", font=("goudy old style", 15), bg="white", fg="black").place(x=750,y=230)
         
        txt_email=Entry(self.root, textvariable=self.var_emp_email, font=("goudy old style", 15), bg="lightyellow", fg="black").place(x=150,y=230, width=180)
        txt_password=Entry(self.root, textvariable=self.var_emp_password, font=("goudy old style", 15), bg="lightyellow", fg="black").place(x=500,y=230, width=180)
        cmb_uType=ttk.Combobox(self.root, textvariable=self.var_emp_uType, values=("Admin", 
        "User"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_uType.place(x=850,y=230,width=180)
        cmb_uType.current(0)


        #====row4=======
        lbl_address=Label(self.root, text="Addresse:", font=("goudy old style", 15), bg="white", fg="black").place(x=50,y=270)
        lbl_salaire=Label(self.root, text="Salaire:", font=("goudy old style", 15), bg="white", fg="black").place(x=500,y=270)
        
        self.txt_address=Text(self.root, font=("goudy old style", 15), bg="lightyellow", fg="black")
        self.txt_address.place(x=150,y=270, width=300, height=60)
        txt_salaire=Entry(self.root, textvariable=self.var_emp_salaire, font=("goudy old style", 15), bg="lightyellow", fg="black").place(x=600,y=270, width=180)
        

        #=====Buttons======
        btn_add=Button(self.root, text="Ajouter", command=self.add, font=("goudy old style", 15), bg="#2196f3", 
        fg="white", cursor="hand2").place(x=500,y=305, width=110, height=28)
        btn_update=Button(self.root, text="Mis-a-jour", command=self.update, font=("goudy old style", 15), bg="#4caf50", 
        fg="white", cursor="hand2").place(x=620,y=305, width=110, height=28)
        btn_delete=Button(self.root, text="Supprimer", command=self.delete, font=("goudy old style", 15), bg="#f44336", 
        fg="white", cursor="hand2").place(x=740,y=305, width=110, height=28)
        btn_clear=Button(self.root, text="Effacer", command=self.clear, font=("goudy old style", 15), bg="#607d8b", 
        fg="white", cursor="hand2").place(x=860,y=305, width=110, height=28)


        #=======Employees Details======
        emp_frame=Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=350, relwidth=1, height=150)

        scolly=Scrollbar(emp_frame, orient=VERTICAL)
        scollx=Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable=ttk.Treeview(emp_frame, columns=("id", "nom", "email", "sexe", "contact", "date_debut", "date_fin", "password", "type", "address", "salaire"), 
        yscrollcommand=scolly.set, xscrollcommand=scollx.set)
        
        scollx.pack(side=BOTTOM, fill=X)
        scolly.pack(side=RIGHT, fill=Y)
        scollx.config(command=self.EmployeeTable.xview)
        scolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("id", text="EMP ID")
        self.EmployeeTable.heading("nom", text="Nom")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("sexe", text="Sexe")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("date_debut", text="Date debut")
        self.EmployeeTable.heading("date_fin", text="Date fin")
        self.EmployeeTable.heading("password", text="Password")
        self.EmployeeTable.heading("type", text="Type")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salaire", text="Salaire")

        self.EmployeeTable["show"]="headings"

        self.EmployeeTable.column("id", width=90)
        self.EmployeeTable.column("nom", width=100)
        self.EmployeeTable.column("email", width=100)
        self.EmployeeTable.column("sexe", width=100)
        self.EmployeeTable.column("contact", width=100)
        self.EmployeeTable.column("date_debut", width=100)
        self.EmployeeTable.column("date_fin", width=100)
        self.EmployeeTable.column("password", width=100)
        self.EmployeeTable.column("type", width=100)
        self.EmployeeTable.column("address", width=100)
        self.EmployeeTable.column("salaire", width=100)
        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

#================   ==  =   =   =   =   =   =   ============
    #========ADD===============================
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()

        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error", "Entrer ID", parent=self.root)
            else:
                cur.execute("Select * from employee where id=?", (self.var_emp_id.get(), ))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error", "ID indisponible, utiliser un autre", parent=self.root)
                else:
                    cur.execute("Insert into employee (id, nom, email, sexe, contact, date_debut, date_fin, password, type, address, salaire) values(?,?,?,?,?,?,?,?,?,?,?)",(
                                        self.var_emp_id.get(),
                                        self.var_emp_nom.get(),
                                        self.var_emp_email.get(),
                                        self.var_emp_sexe.get(),
                                        self.var_emp_contact.get(),

                                        self.var_emp_dateDebut.get(),
                                        self.var_emp_dateFin.get(),

                                        self.var_emp_password.get(),
                                        self.var_emp_uType.get(),
                                        self.txt_address.get('1.0', END),
                                        self.var_emp_salaire.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Succes!", parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        #=======END ADD===========


    #========UPDATE===============================
    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()

        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error", "Entrer ID", parent=self.root)
            else:
                cur.execute("Select * from employee where id=?", (self.var_emp_id.get(), ))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Invalide ID", parent=self.root)
                else:
                    cur.execute("Update employee set nom=?, email=?, sexe=?, contact=?, date_debut=?, date_fin=?, password=?, type=?, address=?, salaire=? where id=?",(
                                        self.var_emp_nom.get(),
                                        self.var_emp_email.get(),
                                        self.var_emp_sexe.get(),
                                        self.var_emp_contact.get(),

                                        self.var_emp_dateDebut.get(),
                                        self.var_emp_dateFin.get(),

                                        self.var_emp_password.get(),
                                        self.var_emp_uType.get(),
                                        self.txt_address.get('1.0', END),
                                        self.var_emp_salaire.get(),
                                        self.var_emp_id.get(),
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
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error", "Entrer ID", parent=self.root)
            else:
                cur.execute("Select * from employee where id=?", (self.var_emp_id.get(), ))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Invalide employé ID", parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm", "Supprimer?", parent=self.root)
                    if op==True:
                        cur.execute("delete from employee where id=?", (self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Succes!", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        #=======END DELETE===========

    #========CLEAR===============================
    def clear(self):
        self.var_emp_id.set(""),
        self.var_emp_nom.set(""),
        self.var_emp_email.set(""),
        self.var_emp_sexe.set("Select"),
        self.var_emp_contact.set(""),

        self.var_emp_dateDebut.set(""),
        self.var_emp_dateFin.set(""),

        self.var_emp_password.set(""),
        self.var_emp_uType.set("Admin"),
        self.txt_address.delete('1.0', END),
        self.var_emp_salaire.set(""), 
        self.var_searchTxt.set(""),
        self.var_searchBy.set("Select")
        self.show()   
    #=======END CLEAR===========

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchBy.get()=="Select": 
                messagebox.showerror("Error", "Selectionner une recherche par option", parent=self.root)
            elif self.var_searchTxt.get()=="":
                messagebox.showerror("Error", "Entrer un terme!", parent=self.root)
            else:  
                cur.execute("Select * from employee where "+self.var_searchBy.get()+" LIKE '%"+self.var_searchTxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "Sans retour!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

        

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)



    #====get data on click to update
    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        #print(row)
        self.var_emp_id.set(row[0]),
        self.var_emp_nom.set(row[1]),
        self.var_emp_email.set(row[2]),
        self.var_emp_sexe.set(row[3]),
        self.var_emp_contact.set(row[4]),

        self.var_emp_dateDebut.set(row[5]),
        self.var_emp_dateFin.set(row[6]),

        self.var_emp_password.set(row[7]),
        self.var_emp_uType.set(row[8]),
        self.txt_address.delete('1.0', END),
        self.txt_address.insert(END, row[9]),
        self.var_emp_salaire.set(row[10]),

if __name__=="__main__":
    root=Tk()
    obj=employeeClass(root)
    root.mainloop()