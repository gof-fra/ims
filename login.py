from tkinter import*
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
import os
import email_password
import smtplib #pip install smtplib
import time
class Login_System:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Système de gestion | developped by else.td")
        self.root.config(bg="white")

        #=========images==========
        self.phone_image1=ImageTk.PhotoImage(file="images/2222.png")
        self.lbl_Phone_image=Label(self.root, image=self.phone_image1, bd=0).place(x=200, y=100)
        self.phone_image2=ImageTk.PhotoImage(file="images/2.png")
        self.lbl_Phone_image=Label(self.root, image=self.phone_image2, bd=0).place(x=300, y=300)


        #=======Login Frame===========
        self.employee_id=StringVar()
        self.password=StringVar()
        login_frame=Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_frame.place(x=650, y=90, width=350, height=460)

        title=Label(login_frame, text="Système d'identification", font=("Elephant", 30, "bold"), bg="green").place(x=0, y=10, relwidth=1)
        
        lbl_user=Label(login_frame, text="N° ID", font=("Andalus", 15), bg="white", fg="#767171").place(x=50, y=100)
        txt_username=Entry(login_frame, textvariable=self.employee_id, font=("times new roman", 15), bg="black").place(x=50, y=140, width=250)

        lbl_password=Label(login_frame, text="Mot de passe", font=("Andalus", 15), bg="white", fg="#767171").place(x=50, y=190)
        txt_password=Entry(login_frame, textvariable=self.password, show="*", font=("times new roman", 15), bg="black").place(x=50, y=240, width=250)

        lbl_login=Button(login_frame, command=self.login, text="Log In", font=("Arial Rounded MT Bold", 15), bg="#00B0F0", activebackground="#00B0F0", fg="white", activeforeground="white").place(x=50, y=300, width=250, height=35)

        hr=Label(login_frame, bg="lightgray").place(x=50, y=360, width=250, height=2)
        or_=Label(login_frame, text="OU", fg="lightgray", bg="white", font=("times new roman", 15, "bold")).place(x=166, y=350)

        btn_forget=Button(login_frame, text="Mot de passe oublié?", command=self.forget_window, font=("times new roman", 13), bg="white", fg="#00759E", bd=0, activeforeground="#00759E", activebackground="white").place(x=100, y=390)


        #==============Frame2===========
        #register_frame=Frame(self.root, bd=2, relief=RIDGE, bg="white")
        #register_frame.place(x=650, y=570, width=350, height=60)


        #lbl_register=Label(register_frame, text="Don't have account ?", font=("times new roman", 13),fg="#00759E", bg="white").place(x=40, y=20)
        #lbl_singup=Button(register_frame, text="Sing Up", font=("Arial Rounded MT Bold", 15, "bold"), bg="#00B0F0", activebackground="#00B0F0", fg="white", activeforeground="white").place(x=210, y=10)

        #========Animation Images==========

        #========All function    ==========


    def login(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror('Error', "Champs obligatoire!", parent=self.root)
            else:
                cur.execute("select type from employee where id=? AND password=?", (self.employee_id.get(), self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror('Error', "Invalide n° ID ou mot de passe", parent=self.root)
                else:
                    #print(user)
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
           messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)



    def forget_window(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror('Error', "Entrer ID", parent=self.root)
            else:
                cur.execute("select email from employee where id=?", (self.employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror('Error', "Invalide ID, réessayer!", parent=self.root)
                else:
                    #=========Forget wondow
                    self.var_otp=StringVar()
                    self.var_new_password=StringVar()
                    self.var_new_password_conf=StringVar()
                    #call send_email_function
                    chk=self.send_email(email[0])
                    if chk=='f':
                        messagebox.showerror("Error", "Connection error, try egain", parent=self.root)
                    else:
                        self.forget_win=Toplevel(self.root)
                        self.forget_win.title('Changer mot de passe')
                        self.forget_win.geometry('400x350+500+100')
                        self.forget_win.focus_force()

                        title=Label(self.forget_win, text='Entrer un nouveau mot de passe!', font=('goudy old style', 15, 'bold'), bg="#3f51b5", fg="white").pack(side=TOP, fill=X)
                        lbl_reset=Label(self.forget_win, text="Entrer le code envoyé dans votre email", font=('times new roman', 15)).place(x=20, y=60)
                        txt_reset=Entry(self.forget_win, textvariable=self.var_otp, font=('times new roman', 15, ), bg="#3f51b5", fg="white").place(x=20, y=100, width=250, height=30)
                        
                        
                        self.btn_reset=Button(self.forget_win, text="Entrer", command=self.validate_otp, font=('times new roman', 15 ), bg="#3f51b5", fg="white")
                        self.btn_reset.place(x=280, y=100, width=100, height=30)

                        #tshngwhbnriaxsrc
                        new_password=Label(self.forget_win, text='Nouveau mot de passe', font=('goudy old style', 15, 'bold'), bg="#3f51b5", fg="white").place(x=20, y=160)
                        txt_new_password=Entry(self.forget_win, textvariable=self.var_new_password, font=('times new roman', 15)).place(x=20, y=190, width=250, height=30)
                        
                        config_password=Label(self.forget_win, text='Confirmer mot de passe', font=('goudy old style', 15, 'bold'), bg="#3f51b5", fg="white").place(x=20, y=225)
                        txt_config_password=Entry(self.forget_win, textvariable=self.var_new_password_conf, font=('times new roman', 15)).place(x=20, y=255, width=250, height=30)
                        
                        self.btn_update=Button(self.forget_win, text="Changer", command=self.update_password, state=DISABLED, font=('times new roman', 15 ), bg="#3f51b5", fg="white")
                        self.btn_update.place(x=150, y=300, width=100, height=30)


        except Exception as ex:
           messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def update_password(self):
        if self.var_new_password.get()=="" or self.var_new_password_conf.get()=="":
            messagebox.showerror("Error", "Password is required", parent=self.forget_win)
        elif self.var_new_password.get()!= self.var_new_password_conf.get():
            messagebox.showerror("Error", "New and confirm password should be same", parent=self.forget_win)
        else:
            con=sqlite3.connect(database=r'ims.db')
            cur=con.cursor()
            try:
                cur.execute("Update employee SET password=? where id=?", (self.var_new_password.get(), self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Success", "Password updated successfully!", parent=self.forget_win)
                self.forget_win.destroy()

            except Exception as ex:
             messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error", "Invalid OTP, try egain", parent=self.forget_win)


    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        email_=email_password.email_
        password_=email_password.password_

        s.login(email_,password_)

        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
        
        subj='IMS-Reset password OTP'
        msg=f'Dear Sir\n\nYour Reset OTP is {str(self.otp)}.\n\n With Regars, \n\nIMS Team'
        msg="Subject:{}\n\n{}".format(subj, msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'

root=Tk()
obj=Login_System(root)
root.mainloop()
