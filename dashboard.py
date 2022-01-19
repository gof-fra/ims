from tkinter import*
from PIL import Image, ImageTk
from employee import employeeClass
from client import clientClass
from category import categoryClass
from product import productClass
from sale import saleClass
import sqlite3
import os
import time
from tkinter import messagebox
class IMS:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Système de gestion | developped by else.td")
        self.root.config(bg="white")

        #===title====
        self.icon_title=PhotoImage(file="images/111.png")
        title=Label(self.root,text="Boulangerie la Baguette", image=self.icon_title, 
        compound=LEFT,font=("times new roman",40,"bold"),bg="#778899",fg="white",anchor="w",
        padx=20).place(x=0,y=0,relwidth=10,height=70)

        #===btn-logout===
        btn_logout=Button(self.root,text="Logout", command=self.logout, font=("times new roman", 15, "bold"), bg="yellow", 
        cursor="hand2").place(x=1100,y=10, height=50, width=150)

        #===clock=====
        self.lbl_clock=Label(self.root,text="Bienvenue dans notre système de gestion!\t\t Date: DD-MM-YYYY\t\t Temps: HH:MM:SS",font=("times new roman",15),bg="#8FBC8F",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #===leftMenu====
        self.MenuLogo=Image.open("images/1.png")
        self.MenuLogo=self.MenuLogo.resize((200, 200),Image.ANTIALIAS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu=Frame(self.root, bd=2,relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=200, height=565)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)

        self.icon_side=PhotoImage(file="images/icone.png")
        lbl_menu=Button(LeftMenu,text="Menu", font=("times new roman", 20), bg="#009688").pack(side=TOP, fill=X)

        btn_employee=Button(LeftMenu,text="Employés", command=self.employee, image=self.icon_side,compound=LEFT, 
                    padx=5, anchor="w", font=("times new roman", 20, "bold"), bg="white",bd=3,
                    cursor="hand2").pack(side=TOP, fill=X)
        btn_client=Button(LeftMenu,text="Clients", command=self.client, image=self.icon_side,compound=LEFT, 
                    padx=5, anchor="w", font=("times new roman", 20, "bold"), 
                    bg="white",bd=3,cursor="hand2").pack(side=TOP, fill=X)
        btn_categories=Button(LeftMenu,text="Categories", command=self.category, image=self.icon_side,compound=LEFT, 
                    padx=5, anchor="w", font=("times new roman", 20, "bold"), bg="white",
                    bd=3,cursor="hand2").pack(side=TOP, fill=X)
        btn_produits=Button(LeftMenu,text="Produits", command=self.product, image=self.icon_side,compound=LEFT, 
                    padx=5, anchor="w", font=("times new roman", 20, "bold"), bg="white",bd=3,
                    cursor="hand2").pack(side=TOP, fill=X)
        btn_vente=Button(LeftMenu,text="Vente", command=self.sale, image=self.icon_side,compound=LEFT, 
                    padx=5, anchor="w", font=("times new roman", 20, "bold"), bg="white",bd=3,
                    cursor="hand2").pack(side=TOP, fill=X)
        btn_exit=Button(LeftMenu,text="Exit", image=self.icon_side,compound=LEFT, 
                    padx=5, anchor="w", font=("times new roman", 20, "bold"), bg="white",
                    bd=3,cursor="hand2").pack(side=TOP, fill=X)

        #====Content====
        self.lbl_employee=Label(self.root, text="Employés\n[ 0 ]", bd=5, relief=RIDGE, 
        bg="#33bbf9", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_employee.place(x=300,y=120,height=150, width=250)

        self.lbl_client=Label(self.root, text="Clients\n[ 0 ]", bd=5, relief=RIDGE, 
        bg="#00FA9A", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_client.place(x=650,y=120,height=150, width=250)

        self.lbl_produit=Label(self.root, text="Produits\n[ 0 ]", bd=5, relief=RIDGE, 
        bg="#F08080", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_produit.place(x=300,y=300,height=150, width=250)


        self.lbl_categories=Label(self.root, text="Categories\n[ 0 ]", bd=5, relief=RIDGE, 
        bg="#008000", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_categories.place(x=1000,y=120,height=150, width=250)

        self.lbl_vente=Label(self.root, text="Vente\n[ 0 ]", bd=5, relief=RIDGE, 
        bg="#FF8C00", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_vente.place(x=650,y=300,height=150, width=250)


        #===footer=====
        lbl_footer=Label(self.root,text="Copyright-2022 | Developped by else.td, All right reserved.", font=("times new roman",20),bg="#8FBC8F",fg="white").pack(side=BOTTOM, fill=X)

        self.update_content()
        #========================================================================================================

    def employee(seft):
        seft.new_win=Toplevel(seft.root)
        seft.new_obj=employeeClass(seft.new_win)


    def client(seft):
        seft.new_win=Toplevel(seft.root)
        seft.new_obj=clientClass(seft.new_win)


    def category(seft):
        seft.new_win=Toplevel(seft.root)
        seft.new_obj=categoryClass(seft.new_win)


    def product(seft):
        seft.new_win=Toplevel(seft.root)
        seft.new_obj=productClass(seft.new_win)


    def sale(seft):
        seft.new_win=Toplevel(seft.root)
        seft.new_obj=saleClass(seft.new_win)
        

    def update_content(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_produit.config(text=f'Produits\n [{str(len(product))}]')

            cur.execute("select * from client")
            client=cur.fetchall()
            self.lbl_client.config(text=f'Clients\n [{str(len(client))}]')

            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_categories.config(text=f'Categories\n [{str(len(category))}]')

            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f'Employés\n [{str(len(employee))}]')

            bill=(len(os.listdir('bill')))

            self.lbl_vente.config(text=f'Vente\n [{str(bill)}]')


            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Bienvenue dans notre système de gestion!!!\t\t Date: {str(date_)}\t\t Temps: {str(time_)}",font=("times new roman",15),bg="#8FBC8F",fg="white")
            self.lbl_clock.after(200,self.update_content)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


    def logout(self):
        self.root.destroy()
        os.system("python login.py")


if __name__=="__main__":
    root=Tk()
    obj=IMS(root)
    root.mainloop()