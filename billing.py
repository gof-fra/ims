from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import tempfile
import subprocess, sys
class billingClass:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Système de gestion | developped by else.td")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0
        #===title====
        self.icon_title=PhotoImage(file="images/111.png")
        title=Label(self.root,text="Boulangerie la Baguette", image=self.icon_title, 
        compound=LEFT,font=("times new roman",40,"bold"),bg="#778899",fg="white",anchor="w",
        padx=20).place(x=0,y=0,relwidth=10,height=70)

        #===btn-logout===
        btn_logout=Button(self.root,text="Logout", command=self.logout, font=("times new roman", 15, "bold"), bg="yellow", 
        cursor="hand2").place(x=1100,y=10, height=50, width=150)

        #===clock=====
        self.lbl_clock=Label(self.root,text="Bienvenue dans notre système de gestion!\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#8FBC8F",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #=======Product_name======
        self.var_search=StringVar()

        #========SEARCH FRAME=========
        ProductFrame1=Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProductFrame1.place(x=6, y=110, width=410, height=550)

        prodTitle=Label(ProductFrame1, text="Produits en Stock", font=("goudy old style", 20, "bold"),bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

        #========PRODUCT SEARCH FRAME=========
        self.var_search=StringVar()
        ProductFrame2=Frame(ProductFrame1, bd=2, relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, width=398, height=90)

        lbl_search=Label(ProductFrame2, text="Rechercher un product | par nom", font=("times new roman", 15, "bold"), bg="white", fg="green").place(x=2, y=5)

        lbl_search=Label(ProductFrame2, text="Entrer nom ", font=("times new roman", 15, "bold"), bg="black").place(x=2, y=45)

        lbl_search=Entry(ProductFrame2, textvariable=self.var_search, font=("times new roman", 15), bg="black").place(x=128, y=47, width=150, height=22)

        btn_search=Button(ProductFrame2, text="Chercher", command=self.search, font=("goudy old style", 15), bg="#2196f3", fg="white").place(x=285, y=45,width=100, height=25)

        btn_show_all=Button(ProductFrame2, text="Afficher ", command=self.show, font=("goudy old style", 15), bg="#083531", fg="white").place(x=285, y=10,width=100, height=25)


        #========PRODUCT DETAIL FRAME=========      cartFrame=ProductFrame3, ProductFrame1=lui, CartTable=product_Table, 
        ProductFrame3=Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=2, y=140, width=395, height=375)

        scolly=Scrollbar(ProductFrame3, orient=VERTICAL)
        scollx=Scrollbar(ProductFrame3, orient=HORIZONTAL)

        self.product_Table=ttk.Treeview(ProductFrame3, columns=("pid", "nom", "prix", "qty", "status"), 
        yscrollcommand=scolly.set, xscrollcommand=scollx.set)
        
        scollx.pack(side=BOTTOM, fill=X)
        scolly.pack(side=RIGHT, fill=Y)
        scollx.config(command=self.product_Table.xview)
        scolly.config(command=self.product_Table.yview)

        self.product_Table.heading("pid", text="PID")
        self.product_Table.heading("nom", text="Nom")
        self.product_Table.heading("prix", text="Prix")
        self.product_Table.heading("qty", text="Quantité")
        self.product_Table.heading("status", text="Status")
        

        self.product_Table["show"]="headings"

        self.product_Table.column("pid", width=40)
        self.product_Table.column("nom", width=100)
        self.product_Table.column("prix", width=100)
        self.product_Table.column("qty", width=40)
        self.product_Table.column("status", width=90)
        
        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)
        lbl_note=Label(ProductFrame1, text="NB: 'Le produit dont la qty=0 sera supprimer de la liste!'", font=("goudy old style", 16), anchor='w', bg="#083531", fg="red").pack(side=BOTTOM, fill=X)

        #========CustomerFrame========
        self.var_cnom=StringVar()
        self.var_contact=StringVar()
        CustomerFrame=Frame(self.root, bd=4, relief=RIDGE, bg="white")
        CustomerFrame.place(x=420, y=110, width=530, height=70)

        cusTitle=Label(CustomerFrame, text="Détails du client", font=("goudy old style", 15),bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)
        lbl_nom=Label(CustomerFrame, text="Nom", font=("times new roman", 15, "bold"), bg="black").place(x=5, y=35)
        txt_nom=Entry(CustomerFrame, textvariable=self.var_cnom, font=("times new roman", 15), bg="black").place(x=80, y=35, width=180)

        lbl_contact=Label(CustomerFrame, text="Contact", font=("times new roman", 15, "bold"), bg="black").place(x=270, y=35)
        txt_contact=Entry(CustomerFrame, textvariable=self.var_contact, font=("times new roman", 15), bg="black").place(x=380, y=35, width=140)

        #========CALCUL CART FRAME=========
        Calcul_cartFrame=Frame(self.root, bd=4, relief=RIDGE, bg="white")
        Calcul_cartFrame.place(x=420, y=190, width=530, height=360)

        #========CALCULATOR FRAME=========
        self.var_cal_input=StringVar()
        Calcul_Frame=Frame(Calcul_cartFrame, bd=9, relief=RIDGE, bg="white")
        Calcul_Frame.place(x=5, y=10, width=268, height=340)

        self.txt_cal_input=Entry(Calcul_Frame, textvariable=self.var_cal_input, font=('arial', 15, 'bold'), width=21, bd=10, relief=GROOVE, state='readonly', justify=RIGHT)
        self.txt_cal_input.grid(row=0, columnspan=4)

        btn_7=Button(Calcul_Frame, text='7', font=('arial', 15, 'bold'), command=lambda:self.get_input(7), bd=5, width=2, pady=18).grid(row=1, column=0)
        btn_8=Button(Calcul_Frame, text='8', font=('arial', 15, 'bold'), command=lambda:self.get_input(8),bd=5, width=2, pady=18).grid(row=1, column=1)
        btn_9=Button(Calcul_Frame, text='9', font=('arial', 15, 'bold'), command=lambda:self.get_input(9),bd=5, width=2, pady=18).grid(row=1, column=2)
        btn_sum=Button(Calcul_Frame, text='+', font=('arial', 15, 'bold'), command=lambda:self.get_input('+'),bd=5, width=2, pady=18).grid(row=1, column=3)

        btn_4=Button(Calcul_Frame, text='4', font=('arial', 15, 'bold'), command=lambda:self.get_input(4),bd=5, width=2, pady=18).grid(row=2, column=0)
        btn_5=Button(Calcul_Frame, text='5', font=('arial', 15, 'bold'), command=lambda:self.get_input(5),bd=5, width=2, pady=18).grid(row=2, column=1)
        btn_6=Button(Calcul_Frame, text='6', font=('arial', 15, 'bold'), command=lambda:self.get_input(6),bd=5, width=2, pady=18).grid(row=2, column=2)
        btn_sub=Button(Calcul_Frame, text='-', font=('arial', 15, 'bold'), command=lambda:self.get_input('-'),bd=5, width=2, pady=18).grid(row=2, column=3)

        btn_1=Button(Calcul_Frame, text='1', font=('arial', 15, 'bold'), command=lambda:self.get_input(1),bd=5, width=2, pady=18).grid(row=3, column=0)
        btn_2=Button(Calcul_Frame, text='2', font=('arial', 15, 'bold'), command=lambda:self.get_input(2),bd=5, width=2, pady=18).grid(row=3, column=1)
        btn_3=Button(Calcul_Frame, text='3', font=('arial', 15, 'bold'), command=lambda:self.get_input(3),bd=5, width=2, pady=18).grid(row=3, column=2)
        btn_mul=Button(Calcul_Frame, text='*', font=('arial', 15, 'bold'), command=lambda:self.get_input('*'),bd=5, width=2, pady=18).grid(row=3, column=3)

        btn_0=Button(Calcul_Frame, text='0', font=('arial', 15, 'bold'), command=lambda:self.get_input(0),bd=5, width=2, pady=18).grid(row=4, column=0)
        btn_c=Button(Calcul_Frame, text='c', font=('arial', 15, 'bold'), command=self.clear_cal,bd=5, width=2, pady=18).grid(row=4, column=1)
        btn_eq=Button(Calcul_Frame, text='=', font=('arial', 15, 'bold'), command=self.perform_cal ,bd=5, width=2, pady=18).grid(row=4, column=2)
        btn_div=Button(Calcul_Frame, text='/', font=('arial', 15, 'bold'), command=lambda:self.get_input('/'),bd=5, width=2, pady=18).grid(row=4, column=3)


        #========CART FRAME=========
        cartFrame=Frame(Calcul_cartFrame, bd=3, relief=RIDGE)
        cartFrame.place(x=280, y=8, width=245, height=342)
        self.cartTitle=Label(cartFrame, text="Cart \t total product: [0]", font=("goudy old style", 15),bg="#0f4d7d", fg="white")
        self.cartTitle.pack(side=TOP, fill=X)
        

        scolly=Scrollbar(cartFrame, orient=VERTICAL)
        scollx=Scrollbar(cartFrame, orient=HORIZONTAL)

        self.CartTable=ttk.Treeview(cartFrame, columns=("pid", "nom", "prix", "qty"), 
        yscrollcommand=scolly.set, xscrollcommand=scollx.set)
        
        scollx.pack(side=BOTTOM, fill=X)
        scolly.pack(side=RIGHT, fill=Y)
        scollx.config(command=self.CartTable.xview)
        scolly.config(command=self.CartTable.yview)

        self.CartTable.heading("pid", text="PID")
        self.CartTable.heading("nom", text="Nom")
        self.CartTable.heading("prix", text="Prix")
        self.CartTable.heading("qty", text="QTY")
        

        self.CartTable["show"]="headings"

        self.CartTable.column("pid", width=40)
        self.CartTable.column("nom", width=90)
        self.CartTable.column("prix", width=90)
        self.CartTable.column("qty", width=40)
        
        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)


        #========ADD CART widgets frame=========
        self.var_pid=StringVar()
        self.var_pnom=StringVar()
        self.var_prix=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()

        Add_CartWidgetsFrame=Frame(self.root, bd=4, relief=RIDGE, bg="white")
        Add_CartWidgetsFrame.place(x=420, y=550, width=530, height=110)

        lbl_p_nom=Label(Add_CartWidgetsFrame, text="Product Nom", font=("times new roman", 15),bg="#0f4d7d", fg="white").place(x=5, y=5)
        txt_p_nom=Entry(Add_CartWidgetsFrame, textvariable=self.var_pnom, font=("times new roman", 15),bg="#0f4d7d", fg="white").place(x=5, y=35, width=190, height=22)

        lbl_p_prix=Label(Add_CartWidgetsFrame, text="Prix par qty", font=("times new roman", 15),bg="#0f4d7d", fg="white").place(x=230, y=5)
        txt_p_prix=Entry(Add_CartWidgetsFrame, textvariable=self.var_prix, font=("times new roman", 15),bg="#0f4d7d", fg="white").place(x=230, y=35, width=150, height=22)

        lbl_p_qty=Label(Add_CartWidgetsFrame, text="Quantité", font=("times new roman", 15),bg="#0f4d7d", fg="white").place(x=390, y=5)
        txt_p_qty=Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, font=("times new roman", 15),bg="#0f4d7d", fg="white").place(x=390, y=35, width=100, height=22)

        self.lbl_inStock=Label(Add_CartWidgetsFrame, text="En Stock", font=("times new roman", 15),bg="#0f4d7d", fg="white")
        self.lbl_inStock.place(x=5, y=70)

        btn_clear_cart=Button(Add_CartWidgetsFrame, text="Effacer", command=self.clear_cart, font=("times new roman", 15), bg="#0f4d7d", fg="white" ).place(x=180, y=70, width=150, height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame, text="Ajouter | Carte", command=self.add_update_cart, font=("times new roman", 15, "bold"), bg="orange", fg="white" ).place(x=340, y=70, width=180, height=30)

#==================Billing Area========
        billFrame=Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billFrame.place(x=953, y=110, width=330, height=410)

        billTitle=Label(billFrame, text="Facture", font=("goudy old style", 20, "bold"),bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)
        scolly=Scrollbar(billFrame, orient=VERTICAL)
        scolly.pack(side=RIGHT, fill=Y)


        self.txt_bill_area=Text(billFrame, yscrollcommand=scolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scolly.config(command=self.txt_bill_area.yview)

        #==================Billing Buttom========
        billMenuFrame=Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billMenuFrame.place(x=953, y=520, width=340, height=140)

        self.lbl_amnt=Label(billMenuFrame, text='Montant\n[0]', font=("goudy old style", 15, "bold"), bg="#3f51b5", fg="white")
        self.lbl_amnt.place(x=2, y=5, width=100, height=70)

        self.lbl_discount=Label(billMenuFrame, text='Reduction\n[1%]', font=("goudy old style", 15, "bold"), bg="#3f51b5", fg="white")
        self.lbl_discount.place(x=124, y=5, width=100, height=70)

        self.lbl_net_pay=Label(billMenuFrame, text='A payer\n[0]', font=("goudy old style", 15, "bold"), bg="#3f51b5", fg="white")
        self.lbl_net_pay.place(x=246, y=5, width=100, height=70)


        btn_print=Button(billMenuFrame, text='Imprimer\nfacture', command=self.print_bill, font=("goudy old style", 15, "bold"), bg="#3f51b5", fg="white")
        btn_print.place(x=2, y=80, width=80, height=50)

        btn_clear_all=Button(billMenuFrame, text='Effacer\n tout', command=self.clear_all, font=("goudy old style", 15, "bold"), bg="#3f51b5", fg="white")
        btn_clear_all.place(x=124, y=80, width=80, height=50)

        btn_generate=Button(billMenuFrame, text='Générer\n Facture', command=self.generate_bill, font=("goudy old style", 15, "bold"), bg="#3f51b5", fg="white")
        btn_generate.place(x=246, y=80, width=80, height=50)


        #===footer=====
        lbl_footer=Label(self.root,text="Copyright-2022 | Developped by else.td, All right reserved."
        ,font=("times new roman",20),bg="#8FBC8F",fg="white").pack(side=BOTTOM, fill=X)


        self.show()
        #self.bill_top(),
        self.update_date_time()
#===============ALL FUNCTIONS============
    def get_input(self, num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')


    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))


    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select pid, nom, prix, qty, status from product where status='Actif'")   # select pid, nom, prix, qty, status from product  / Select * from product
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error", "Search input should required", parent=self.root)
            else:  
                cur.execute("select pid, nom, prix, qty, status from product where nom LIKE '%"+self.var_search.get()+"%' and status='Actif'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


    def get_data(self,ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pnom.set(row[1])
        self.var_prix.set(row[2])
        self.lbl_inStock.config(text=f"In Stock[{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')


    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        #pid, nom, prix, qty, stock
        self.var_pid.set(row[0])
        self.var_pnom.set(row[1])
        self.var_prix.set(row[2])
        self.lbl_inStock.config(text=f"In Stock[{str(row[4])}]")
        self.var_stock.set(row[4])
        self.var_qty.set(row[3])
        
    
    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error', "Please select the product from the list", parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror('Error', "Quantity is required", parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror('Error', "Invalid Quantity", parent=self.root)
        else:
            #price_cal=int(self.var_qty.get())*float(self.var_prix.get())
            #price_cal=float(price_cal)
            #print(price_cal)
            price_cal=self.var_prix.get()
            #pid, nom, prix, qty, stock
            cart_date=[self.var_pid.get(), self.var_pnom.get(), price_cal, self.var_qty.get(), self.var_stock.get()]
            #========update_cart======
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            
            if present=='yes':
                op=messagebox.askyesno('Confirm', "Product already present \nDo u want to update? | Remove from the list", parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #pid, nom, prix, qty, status
                        #self.cart_list[index_][2]=price_cal #price
                        self.cart_list[index_][3]=self.var_qty.get() #qty
            else:
                self.cart_list.append(cart_date)
            self.show_cart()
            self.bill_updates()
    

    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            #pid, nom, prix, qty, stock
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
        self.discount=(self.bill_amnt*1)/100
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f'Montant\n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'A Payer\n{str(self.net_pay)}')
        self.cartTitle.config(text=f"Cart \t total product: [{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)



    def generate_bill(self):
        if self.var_cnom.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error", f"Customer Details are required", parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error", f"Please add  product to the cart!!!", parent=self.root)
        else:
            #======Bill Top=========
            self.bill_top()
            #======Bill Middle======
            self.bill_middle()
            #======Bill Bottom======
            self.bill_bottom()


            fp=open(f'bill/{str(self.invoice)}.txt', 'w')
            fp.write(self.txt_bill_area.get('1.0', END))
            fp.close()
            messagebox.showerror('Saved', "Générer/Sauvegarder", parent=self.root)
            self.chk_print=1


    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\tBoulangerie-Baguette d'or
\tTél: 66602010, NDjamena-Tchad
{str("="*43)}
Nom client: {self.var_cnom.get()}
Télephone n°: {self.var_contact.get()}
N° facture: {str(self.invoice)}\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*43)}
Nom produit\t\tQTY\t\tPrix
{str("="*43)}
        '''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)

    
    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*43)}
Montant\t\t\t\t{self.bill_amnt}\tF
Reduction\t\t\t\t{self.discount}\tF
A Payer\t\t\t\t{self.net_pay}\tF
{str("="*43)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)

    

    def bill_middle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                nom=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactif'
                if int(row[3])!=int(row[4]):
                    status='Actif'

                prix=float(row[2])*int(row[3])
                prix=str(prix)
                self.txt_bill_area.insert(END, "\n"+nom+"\t\t\t"+row[3]+"\t"+prix+"\tF")
                #=========Upadte product qty table========== 
                cur.execute('Update product set qty=?, status=? where pid=?',(
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)



    def clear_cart(self):
        self.var_pid.set('')
        self.var_pnom.set('')
        self.var_prix.set('')
        self.lbl_inStock.config(text=f"In Stock[{str('')}]")
        self.var_stock.set('')
        self.var_qty.set('')


    def clear_all(self):
        del self.cart_list[:]
        self.var_cnom.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0', END)
        self.cartTitle.config(text=f"Cart \t total product: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()


    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Bienvenue dans notre système de gestion!!!\t\t Date: {str(date_)}\t\t Temps: {str(time_)}",font=("times new roman",15),bg="#8FBC8F",fg="white")
        self.lbl_clock.after(200,self.update_date_time)


    def print_bill(self):
        if self.chk_print==1:
            messagebox.showerror('Print', "Please wait while printing", parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file, 'w').write(self.txt_bill_area.get('1.0', END))
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, new_file])

        else:
            messagebox.showerror('Print', "Print", parent=self.root)  


    def logout(self):
        self.root.destroy()
        os.system("python login.py")
            
            
if __name__=="__main__":
    root=Tk()
    obj=billingClass(root)
    root.mainloop()