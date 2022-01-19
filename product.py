from tkinter import*
from tkinter import font
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
class productClass:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1100x500+0+0")
        self.root.title("Système de gestion | developped by else.td")
        self.root.config(bg="white")
        self.root.focus_force()

         #===========All Variables =======
        self.var_searchBy=StringVar()
        self.var_searchTxt=StringVar()

        
        #=========================
        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_cli=StringVar()
        self.cat_list=[]
        self.cli_list=[]

        self.fetch_cat_cli()

        self.var_nom=StringVar()
        self.var_prix=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()


        product_Frame=Frame(self.root, bd=2, relief=RIDGE, bg="white")
        product_Frame.place(x=10,y=10, width=450, height=480)

        #======Title====
        title=Label(product_Frame, text="Informations products",font=("goudy old style", 15),
        bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)


         #=======col1=====
        lbl_category=Label(product_Frame, text="Categorie:",font=("goudy old style", 18), bg="#0f4d7d", fg="white").place(x=30, y=60)
        lbl_client=Label(product_Frame, text="Client:",font=("goudy old style", 18), bg="#0f4d7d", fg="white").place(x=30, y=110)
        lbl_nom=Label(product_Frame, text=" Nom:",font=("goudy old style", 18), bg="#0f4d7d", fg="white").place(x=30, y=160)
        lbl_prix=Label(product_Frame, text="Prix:",font=("goudy old style", 18), bg="#0f4d7d", fg="white").place(x=30, y=210)
        lbl_qty=Label(product_Frame, text="Quantité:",font=("goudy old style", 18), bg="#0f4d7d", fg="white").place(x=30, y=260)
        lbl_status=Label(product_Frame, text="Status:",font=("goudy old style", 18), bg="#0f4d7d", fg="white").place(x=30, y=310)
      
        txt_category=Label(product_Frame, text="Categorie:",font=("goudy old style", 18), bg="#0f4d7d", fg="white").place(x=30, y=60)
           #=======option=====

        #=======col2=====
        cmb_cat=ttk.Combobox(product_Frame, textvariable=self.var_cat, values=self.cat_list, state='readonly', justify=CENTER, font=("goudy old style", 15), )
        cmb_cat.place(x=150, y=60, width=200)
        cmb_cat.current(0)


        cmb_cli=ttk.Combobox(product_Frame, textvariable=self.var_cli, values=self.cli_list, state='readonly', justify=CENTER, font=("goudy old style", 15), )
        cmb_cli.place(x=150, y=100, width=200)
        cmb_cli.current(0)


        txt_nom=Entry(product_Frame, textvariable=self.var_nom, font=("goudy old style", 15), bg="#184a45", fg="lightyellow").place(x=150, y=160, width=200)
        txt_prix=Entry(product_Frame, textvariable=self.var_prix, font=("goudy old style", 15), bg="#184a45", fg="lightyellow").place(x=150, y=210, width=200)
        txt_qty=Entry(product_Frame, textvariable=self.var_qty, font=("goudy old style", 15), bg="#184a45", fg="lightyellow").place(x=150, y=260, width=200)

        cmb_status=ttk.Combobox(product_Frame, textvariable=self.var_status, values=("Actif", "Inactif"), state='readonly', justify=CENTER, font=("goudy old style", 15), )
        cmb_status.place(x=150, y=310, width=200)
        cmb_status.current(0)


        #=====Buttons======
        btn_add=Button(product_Frame, text="Ajouter", command=self.add, font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=10,y=400, width=100, height=40)
        btn_update=Button(product_Frame, text="Mis-a-jour", command=self.update, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=120,y=400, width=100, height=40)
        btn_delete=Button(product_Frame, text="Supprimer", command=self.delete, font=("goudy old style", 15), bg="#f44336", fg="white", cursor="hand2").place(x=230,y=400, width=100, height=40)
        btn_clear=Button(product_Frame, text="Effacer", command=self.clear, font=("goudy old style", 15), bg="#607d8b", fg="white", cursor="hand2").place(x=340,y=400, width=100, height=40)

        #=======search=======
        SearchFrame=LabelFrame(self.root,text="Rechercher produits",font=("goudy old style", 12, "bold"), bd=2, relief=RIDGE, bg="green")
        SearchFrame.place(x=480,y=10,width=600,height=80)


        #=======option=====
        cmb_search=ttk.Combobox(SearchFrame, textvariable=self.var_searchBy, values=("Select", "Categorie", "Client", "Nom"), state='readonly', justify=CENTER, font=("goudy old style", 15), )
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame, textvariable=self.var_searchTxt, font=("goudy old style", 15), bg="gray").place(x=200, y=10)
        btn_search=Button(SearchFrame, text="Chercher", command=self.search, font=("goudy old style", 15), bg="gray", fg="white").place(x=410,y=10, width=150, height=30)

        #=======Products Details======
        prod_Frame=Frame(self.root, bd=3, relief=RIDGE)
        prod_Frame.place(x=480, y=100, width=600, height=390)

        scolly=Scrollbar(prod_Frame, orient=VERTICAL)
        scollx=Scrollbar(prod_Frame, orient=HORIZONTAL)

        self.product_table=ttk.Treeview(prod_Frame, columns=("pid", "category", "client", "nom", "prix", "qty", "status"), 
        yscrollcommand=scolly.set, xscrollcommand=scollx.set)
        
        scollx.pack(side=BOTTOM, fill=X)
        scolly.pack(side=RIGHT, fill=Y)
        scollx.config(command=self.product_table.xview)
        scolly.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="Prod ID")
        self.product_table.heading("category", text="Categorie")
        self.product_table.heading("client", text="Client")
        self.product_table.heading("nom", text="Nom")
        self.product_table.heading("prix", text="Prix")
        self.product_table.heading("qty", text="Qty")
        self.product_table.heading("status", text="Status")

        self.product_table["show"]="headings"

        self.product_table.column("pid", width=90)
        self.product_table.column("category", width=100)
        self.product_table.column("client", width=100)
        self.product_table.column("nom", width=100)
        self.product_table.column("prix", width=100)
        self.product_table.column("qty", width=100)
        self.product_table.column("status", width=100)
        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    #================   ==  =   =   ================
    def fetch_cat_cli(self):
        self.cat_list.append("Empty")
        self.cli_list.append("Empty")
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select nom from category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            
            cur.execute("Select nom from client")
            cli=cur.fetchall()
            if len(cli)>0:
                del self.cli_list[:]
                self.cli_list.append("Select")
                for i in cli:
                    self.cli_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


    #========ADD===============================
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()

        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_cli.get()=="Select" or self.var_cli.get()=="Empty":
                messagebox.showerror("Error", "Remplissez tous les champs", parent=self.root)
            else:
                cur.execute("Select * from product where nom=?", (self.var_nom.get(), ))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error", "Produit present", parent=self.root)
                else:
                    cur.execute("Insert into product (category, client, nom, prix, qty, status) values(?,?,?,?,?,?)",(
                                        self.var_cat.get(),
                                        self.var_cli.get(),
                                        self.var_nom.get(),
                                        self.var_prix.get(),
                                        self.var_qty.get(),
                                        self.var_status.get(),
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
            if self.var_pid.get()=="":
                messagebox.showerror("Error", "Selectionner sur la liste", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?", (self.var_pid.get(), ))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Invalide produit", parent=self.root)
                else:
                    cur.execute("Update product set category=?, client=?, nom=?, prix=?, qty=?, status=? where pid=?",(
                                        self.var_cat.get(),
                                        self.var_cli.get(),
                                        self.var_nom.get(),
                                        self.var_prix.get(),
                                        self.var_qty.get(),
                                        self.var_status.get(),
                                        self.var_pid.get(),
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
            if self.var_pid.get()=="":
                messagebox.showerror("Error", "Selectionner sur la liste", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?", (self.var_pid.get(), ))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Invalide produit", parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm", "Supprimer?", parent=self.root)
                    if op==True:
                        cur.execute("delete from product where pid=?", (self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Succes", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        #=======END DELETE===========

    #========CLEAR===============================
    def clear(self):
        self.var_cat.set("Select"),
        self.var_cli.set("Select"),
        self.var_nom.set(""),
        self.var_prix.set(""),
        self.var_qty.set(""),
        self.var_status.set("Active"),
        self.var_pid.set(""),

        self.var_searchTxt.set(""),
        self.var_searchBy.set("Select")
        self.show()   
    #=======END CLEAR===========

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchBy.get()=="Select": 
                messagebox.showerror("Error", "Rechercher par option", parent=self.root)
            elif self.var_searchTxt.get()=="":
                messagebox.showerror("Error", "Entrer terme", parent=self.root)
            else:  
                cur.execute("Select * from product where "+self.var_searchBy.get()+" LIKE '%"+self.var_searchTxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "Sans succes!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

        

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from product")
            rows=cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)



    #====get data on click to update
    def get_data(self,ev):
        f=self.product_table.focus()
        content=(self.product_table.item(f))
        row=content['values']
        self.var_pid.set(row[0]),
        self.var_cat.set(row[1]),
        self.var_cli.set(row[2]),
        self.var_nom.set(row[3]),
        self.var_prix.set(row[4]),
        self.var_qty.set(row[5]),
        self.var_status.set(row[6]),


if __name__=="__main__":
    root=Tk()
    obj=productClass(root)
    root.mainloop()