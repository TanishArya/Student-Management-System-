from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import mysql.connector


def login():        
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="db1"
    )
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM login WHERE username = %s AND password = %s", (EU.get(), EP.get()))
    result = mycursor.fetchone()
    
    if result:
        messagebox.showinfo("Login Successful", "Welcome to the application")
        display.destroy()
        import main
    elif EU.get() == "" or EP.get() == "":
        messagebox.showerror("Error","Please enter username and password")
    else:
        messagebox.showerror("Error","invailid username and password")
           


display = Tk()
display.geometry("1280x700+0+0")
display.title("Student Management System")
bg = ImageTk.PhotoImage(file="bg.jpg")
bgl = Label(display, image=bg)
bgl.place(x=0, y=0)

Frame1 = Frame(display,bg = "white")
Frame1.place(x=400, y=150)
logo = ImageTk.PhotoImage(file="logo.png")
l_image = Label(Frame1, image=logo)
l_image.grid(row=0, column=0,columnspan=2,pady=10)   


u_img = ImageTk.PhotoImage(file="user.png")
username =Label(Frame1,image=u_img, text="Username", font=("Times New Roman", 20, "bold"), fg="black", bg="white",compound=LEFT)
username.grid(row=1, column=0 ,pady=10,padx=20)

EU = Entry(Frame1, font=("Times New Roman", 20, "bold"), fg="black", bg="white", bd=5,foreground="royalblue")
EU.grid(row=1, column=1,pady=10,padx=20)

p_img = ImageTk.PhotoImage(file="Password.png")
passward =Label(Frame1,image=p_img, text="Password", font=("Times New Roman", 20, "bold"), fg="black", bg="white",compound=LEFT)
passward.grid(row=2, column=0 ,pady=10,padx=20)

EP = Entry(Frame1, font=("Times New Roman", 20, "bold"), fg="black", bg="white", bd=5,foreground="royalblue",show="*")
EP.grid(row=2, column=1,pady=10,padx=20)

lb = Button(Frame1, text="Login", font=("Times New Roman", 15, "bold"), fg="white", bg="cornflowerblue",activebackground='cornflowerblue',activeforeground='cornflowerblue',bd=5,cursor='hand2',command=login)
lb.grid(row=3, column=1, pady=10, padx=20)




 





display.mainloop()