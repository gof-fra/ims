from tkinter import*
from tkinter import font
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
class categoryClass:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1100x500+0+0")
        self.root.title("Système de gestion | developped by else.td")
        self.root.config(bg="white")
        self.root.focus_force()

        #======variable======
        self.var_cat_id=StringVar()
        self.var_cat_nom=StringVar()

        lbl_title=Label(self.root, text="Gestion categorie", font=("goudy old style", 30), bg="#184a45", fg="white", bd=3, relief=RIDGE).pack(side=TOP, fill=X, padx=10, pady=20)

        lbl_title=Label(self.root, text="Entrer nom:", font=("goudy old style", 30),bg="#184a45", fg="white").place(x=50, y=100)
        lbl_title=Entry(self.root, textvariable=self.var_cat_nom, font=("goudy old style", 18), bg="#184a45", fg="lightyellow").place(x=50, y=170, width=300)
    
        btn_add=Button(self.root, text="Ajouter", command=self.add, font=("goudy old style", 15), bg="#4caf50", fg="white").place(x=360, y=170, height=30,width=150)
        btn_delete=Button(self.root, text="Supprimer", command=self.delete, font=("goudy old style", 15), bg="red", fg="white").place(x=520, y=170, height=30,width=150)
    

        #=======Category Details======
        cat_frame=Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=700, y=100, width=380, height=100)

        scolly=Scrollbar(cat_frame, orient=VERTICAL)
        scollx=Scrollbar(cat_frame, orient=HORIZONTAL)

        self.CategoryTable=ttk.Treeview(cat_frame, columns=("cid", "nom"), 
        yscrollcommand=scolly.set, xscrollcommand=scollx.set)
        
        scollx.pack(side=BOTTOM, fill=X)
        scolly.pack(side=RIGHT, fill=Y)
        scollx.config(command=self.CategoryTable.xview)
        scolly.config(command=self.CategoryTable.yview)

        self.CategoryTable.heading("cid", text="Cat. ID")
        self.CategoryTable.heading("nom", text="Nom")
        

        self.CategoryTable["show"]="headings"

        self.CategoryTable.column("cid", width=90)
        self.CategoryTable.column("nom", width=100)
        
        self.CategoryTable.pack(fill=BOTH, expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>", self.get_data)



        #=======Image=========
        self.img1=Image.open("images/1.png")
        self.img1=self.img1.resize((500,200),Image.ANTIALIAS)
        self.img1=ImageTk.PhotoImage(self.img1)

        self.lbl_img1=Label(self.root, image=self.img1, bd=2, relief=RAISED)
        self.lbl_img1.place(x=50, y=220)


        self.img2=Image.open("images/1.png")
        self.img2=self.img2.resize((500,200),Image.ANTIALIAS)
        self.img2=ImageTk.PhotoImage(self.img2)

        self.lbl_img2=Label(self.root, image=self.img2, bd=2, relief=RAISED)
        self.lbl_img2.place(x=580, y=220)


        self.show()
         #========ADD===============================
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()

        try:
            if self.var_cat_nom.get()=="":
                messagebox.showerror("Error", "Entrer nom!", parent=self.root)
            else:
                cur.execute("Select * from category where nom=?", (self.var_cat_nom.get(), ))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error", "Cette categorie existe, essayer autre!", parent=self.root)
                else:
                    cur.execute("Insert into category (nom) values(?)",( self.var_cat_nom.get(), ))
                    con.commit()
                    messagebox.showinfo("Success", "Succes!", parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        #=======END ADD===========


     #========DELETE===============================
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()

        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error", "Selectionner sur la liste!", parent=self.root)
            else:
                cur.execute("Select * from category where cid=?", (self.var_cat_id.get(), ))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Error°", parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm", "Supprimer?", parent=self.root)
                    if op==True:
                        cur.execute("delete from category where cid=?", (self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Succes", parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_cat_nom.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        #=======END DELETE===========


    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from category")
            rows=cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)



    #====get data on click to update
    def get_data(self, ev):
        f=self.CategoryTable.focus()
        content=(self.CategoryTable.item(f))
        row=content['values']
        #print(row)
        self.var_cat_id.set(row[0]),
        self.var_cat_nom.set(row[1]),


if __name__=="__main__":
    root=Tk()
    obj=categoryClass(root)
    root.mainloop()