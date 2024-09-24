from tkinter import * 
from tkinter import PhotoImage
from tkinter import ttk
from tkinter import Scrollbar
import mysql.connector
from tkinter import messagebox,filedialog
import pandas


display = Tk()

def clock():
    import time
    import datetime

    time = time.strftime("%H:%M:%S %p")
    datetime = datetime.datetime.now().strftime("%d-%m-%Y")
    datetimelable.config(text=f"Time : {time}\nDate : {datetime}")
    datetimelable.after(1000, clock)
    
    
global mycursor,mydb 
def con():  
    def db():
        try:
            global mycursor,mydb 
            mydb=mysql.connector.connect(
            host = f'{hostnameentry.get()}',
            user = f'{usernameentry.get()}',
            password = f'{passwentry.get()}',
            database = "db1"
            )
            mycursor = mydb.cursor()
            messagebox.showinfo("Database Connection", "Database Connected",parent = dbframe)
            dbframe.destroy()    
        except Exception as f:
            messagebox.showerror("Database Connection", parent = dbframe)
    
    dbframe=Toplevel()
    dbframe.geometry("450x250+0+0")
    dbframe.grab_set()
    dbframe.title("Database Connection")
    dbframe.resizable(0,0)
    
    hostname = Label(dbframe, text="Hostname", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    hostname.grid(row=0, column=0,padx=30,pady=10)
    hostnameentry = Entry(dbframe, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5,)
    hostnameentry.grid(row=0, column=1, padx=30,pady=10)
    
    username = Label(dbframe, text="Username", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    username.grid(row=1, column=0,padx=30,pady=10)
    usernameentry = Entry(dbframe, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5)
    usernameentry.grid(row=1, column=1, padx=30,pady=10)
     
    passw = Label(dbframe, text="Passward", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    passw.grid(row=2, column=0,padx=30,pady=10)
    passwentry = Entry(dbframe, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5,show="*")
    passwentry.grid(row=2, column=1, padx=30,pady=10)
    

    enterbutton = Button(dbframe, text="Enter", font=("Times New Roman", 10, "bold"), fg="white", bg="cornflowerblue", activebackground='black', activeforeground='red', bd=5, cursor='hand2', command=db)
    enterbutton.grid(row=3, column=1, padx=30, pady=10) 

def add_student():
    def add_data():
        if identry.get() == "" or nameentry.get() =="" or addressentry.get() =="" or emailentry.get() =="" or passwordentry.get() =="":
            messagebox.showerror("Error", "All fields are required")
        else:
            try:
                sql = "insert into student_b(s_id,s_name,s_add,s_email,s_pass) values(%s,%s,%s,%s,%s)"
                val = (identry.get(), nameentry.get(), addressentry.get(), emailentry.get(), passwordentry.get())
                mycursor.execute(sql, val)
                mydb.commit()
                messagebox.showinfo("Student Management System", "Student Added Successfully") 
                addwindow.destroy()
                show_student()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
            except NameError:
                messagebox.showerror("Error", "Please connect to the database")
    addwindow = Toplevel()
    
    idlable = Label(addwindow, text="ID", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    idlable.grid(row=0, column=0, padx=30, pady=10)
    identry = Entry(addwindow, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5)
    identry.grid(row=0, column=1, padx=30, pady=10)
    
    namelable = Label(addwindow, text="Name", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    namelable.grid(row=1, column=0, padx=30, pady=10)
    nameentry = Entry(addwindow, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5)
    nameentry.grid(row=1, column=1, padx=30, pady=10)
    
    addresslable = Label(addwindow, text="Address", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    addresslable.grid(row=2, column=0, padx=30, pady=10)
    addressentry = Entry(addwindow, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5)
    addressentry.grid(row=2, column=1, padx=30, pady=10)
    
    emaillable = Label(addwindow, text="Email", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    emaillable.grid(row=3, column=0, padx=30, pady=10)
    emailentry = Entry(addwindow, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5)
    emailentry.grid(row=3, column=1, padx=30, pady=10)
    
    passwordlable = Label(addwindow, text="Passward", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    passwordlable.grid(row=4, column=0, padx=30, pady=10)
    passwordentry = Entry(addwindow, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5,show='*')
    passwordentry.grid(row=4, column=1, padx=30, pady=10)
    
    addbutton = Button(addwindow, text="Add", font=("Times New Roman", 10, "bold"), fg="white", bg="cornflowerblue", activebackground='black', activeforeground='red', bd=5, cursor='hand2', command=add_data)
    addbutton.grid(row=5, column=1, padx=30, pady=10)


def search_student():
    try:
        def search_data():
            fields = {
                's_id': id.get(),
                's_name': name.get(),
                's_add': add.get(),
                's_email': email.get()
            }
            
            # Filter out empty fields
            filled_fields = {k: v for k, v in fields.items() if v}
            
            if not filled_fields:
                messagebox.showerror("Error", "Please enter at least one field")
                return
            
            # Construct the SQL query
            sql = "SELECT * FROM student_b WHERE " + " AND ".join(f"{k} = %s" for k in filled_fields)
            val = tuple(filled_fields.values())
            
            mycursor.execute(sql, val)
            st_table.delete(*st_table.get_children())
            data = mycursor.fetchall()
            
            if data:
                for i in data:
                    st_table.insert("", END, values=i)
            else:
                messagebox.showinfo("Student Management System", "No Student Found")
                searchwindow.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")
    except NameError:
        messagebox.showerror("Error", "Please connect to the database")

            
    searchwindow = Toplevel()
        
    idlable = Label(searchwindow, text="ID", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    idlable.grid(row=0, column=0, padx=30, pady=10)
    id = Entry(searchwindow, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5)
    id.grid(row=0, column=1, padx=30, pady=10)
    
    namelable = Label(searchwindow, text="Name", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    namelable.grid(row=1, column=0, padx=30, pady=10)
    name = Entry(searchwindow, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5)
    name.grid(row=1, column=1, padx=30, pady=10)
    
    addresslable = Label(searchwindow, text=" Address", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    addresslable.grid(row=2, column=0, padx=30, pady=10)
    add = Entry(searchwindow, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5)
    add.grid(row=2, column=1, padx=30, pady=10)
    
    emaillable = Label(searchwindow, text=" Email", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    emaillable.grid(row=3, column=0, padx=30, pady=10)
    email = Entry(searchwindow, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5)
    email.grid(row=3, column=1, padx=30, pady=10)
        
    addbutton = Button(searchwindow, text="Search", font=("Times New Roman", 10, "bold"), fg="white", bg="cornflowerblue", activebackground='black', activeforeground='red', bd=5, cursor='hand2', command=search_data)
    addbutton.grid(row=5, column=1, padx=30, pady=10)  


def delete_student():
    def delete_data():
        try :
            mycursor = mydb.cursor()
            sql ="select * from student_b where s_id = %s and s_pass = %s"
            val = (id.get(),password.get())
            mycursor.execute(sql, val)
            result = mycursor.fetchone()
            if id.get() == "" or password.get() =="":
                messagebox.showerror("Error", "All fields are required")
            elif result:
                pass
                sql ="delete from student_b where s_id = %s"
                val = (id.get(),)
                mycursor.execute(sql, val)
                mydb.commit()
                messagebox.showinfo("Student Management System", "Student Deleted Successfully")
                deletewindow.destroy()
                show_student()
            else:
                messagebox.showerror("Error", "Invalid ID or Password")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
        except NameError:
            messagebox.showerror("Error", "Please connect to the database")
        
    deletewindow = Toplevel()
        
    idlable = Label(deletewindow, text="ID", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    idlable.grid(row=0, column=0, padx=30, pady=10)
    id = Entry(deletewindow, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5)
    id.grid(row=0, column=1, padx=30, pady=10)
    
    passwordlable = Label(deletewindow, text="Passward", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    passwordlable.grid(row=4, column=0, padx=30, pady=10)
    password = Entry(deletewindow, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5,show='*')
    password.grid(row=4, column=1, padx=30, pady=10)
    
    addbutton = Button(deletewindow, text="Delete", font=("Times New Roman", 10, "bold"), fg="white", bg="cornflowerblue", activebackground='black', activeforeground='red', bd=5, cursor='hand2', command=delete_data)
    addbutton.grid(row=5, column=1, padx=30, pady=10)    

def update_student():
    def update_data():
        if id.get() == "" or name.get() == "" or add.get() == "" or email.get() == "":
            messagebox.showerror("Error", "All fields are required")
        else:        
            try :
                sql ="update student_b set s_name = %s ,s_add = %s,s_email = %s where s_id = %s;"
                val = (name.get(), add.get(), email.get(), id.get())
                mycursor.execute(sql,val)
                mydb.commit()
                messagebox.showinfo("Student Management System", "Student Updated Successfully")
                updatewindow.destroy()
                show_student()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
            except NameError:
                messagebox.showerror("Error", "Please connect to the database")
        
    updatewindow = Toplevel()
        
    idlable = Label(updatewindow, text="ID", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    idlable.grid(row=0, column=0, padx=30, pady=10)
    id = Entry(updatewindow, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5)
    id.grid(row=0, column=1, padx=30, pady=10)
    
    namelable = Label(updatewindow, text="New Name", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    namelable.grid(row=1, column=0, padx=30, pady=10)
    name = Entry(updatewindow, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5)
    name.grid(row=1, column=1, padx=30, pady=10)
    
    addresslable = Label(updatewindow, text="New Address", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    addresslable.grid(row=2, column=0, padx=30, pady=10)
    add = Entry(updatewindow, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5)
    add.grid(row=2, column=1, padx=30, pady=10)
    
    emaillable = Label(updatewindow, text="New Email", font=("Times New Roman", 10, "bold"), fg="black", bg="white")
    emaillable.grid(row=3, column=0, padx=30, pady=10)
    email = Entry(updatewindow, font=("Times New Roman", 10, "bold"), fg="black", bg="white", bd=5)
    email.grid(row=3, column=1, padx=30, pady=10)
        
    addbutton = Button(updatewindow, text="Update", font=("Times New Roman", 10, "bold"), fg="white", bg="cornflowerblue", activebackground='black', activeforeground='red', bd=5, cursor='hand2', command=update_data)
    addbutton.grid(row=5, column=1, padx=30, pady=10)    

def show_student():
    try:
        mycursor.execute("select * from student_b")
        data = mycursor.fetchall()
        st_table.delete(*st_table.get_children())
        for i in data:
            li = list(i)
            st_table.insert(parent='', index='end', values=li)
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")
    except NameError:
        messagebox.showerror("Error", "Please connect to the database")
        


def export_student():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = st_table.get_children()
    newdata = []
    for i in indexing:
        content = st_table.item(i)
        data = content['values']
        newdata.append(data)

    table = pandas.DataFrame(newdata, columns=['ID', 'Name', 'Address', 'Email', 'Password'])
    table.to_csv(url, index=False, header=True)

    messagebox.showinfo("Student Management System", "Student Data Saved Successfully")

def exit():
    display.destroy()

    
count = 0
text = ""    
def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ""
    text = text + s[count]
    sliderlable.config(text=text)
    count += 1
    sliderlable.after(300, slider)
    
    

display.geometry("1280x700+0+0")
display.title("Student Management System")

datetimelable = Label(display, text=clock, font=("Times New Roman", 20, "bold"), fg="black", bg="white")
datetimelable.place(x=50, y=20)
clock()


s = "Welcome to Student Management System"
sliderlable = Label(display, text=slider, font=("Times New Roman", 20, "bold"), fg="black", bg="white")
sliderlable.place(x=450, y=20)
slider()

connectdb = Button(display, text="Connect Database", font=("Times New Roman", 15, "bold"), fg="white", bg="cornflowerblue",activebackground='black',activeforeground='red',bd=5,cursor='hand2',command=con)
connectdb.place(x=1050, y=20)


leftframe = Frame(display, bg="white")
leftframe.place(x=50, y=100,height=500,width=350)

logoimage = PhotoImage(file="st.png")
logo = Label(leftframe, image=logoimage, bg="white")
logo.grid(row=0, column=0 ,padx=125,pady=20)

asb = Button(leftframe, text="Add Student", font=("Times New Roman", 10, "bold"), fg="white", bg="cornflowerblue", activebackground='black', activeforeground='red', bd=5, cursor='hand2',width=25,command=add_student)
asb.grid(row=1, column=0, padx=30,pady=10) 

ss = Button(leftframe, text="Search Student", font=("Times New Roman", 10, "bold"), fg="white", bg="cornflowerblue", activebackground='black', activeforeground='red', bd=5, cursor='hand2',width=25,command=search_student)
ss.grid(row=2, column=0, padx=30,pady=10)

ds = Button(leftframe, text="Delete Student", font=("Times New Roman", 10, "bold"), fg="white", bg="cornflowerblue", activebackground='black', activeforeground='red', bd=5, cursor='hand2',width=25,command=delete_student)
ds.grid(row=3, column=0, padx=30,pady=10)

us = Button(leftframe, text="Update Student", font=("Times New Roman", 10, "bold"), fg="white", bg="cornflowerblue", activebackground='black', activeforeground='red', bd=5, cursor='hand2',width=25,command=update_student)
us.grid(row=4, column=0, padx=30,pady=10)

show = Button(leftframe, text="Show Student", font=("Times New Roman", 10, "bold"), fg="white", bg="cornflowerblue", activebackground='black', activeforeground='red', bd=5, cursor='hand2',width=25,command=show_student)
show.grid(row=5, column=0, padx=30,pady=10)

ed = Button(leftframe, text="Export Data", font=("Times New Roman", 10, "bold"), fg="white", bg="cornflowerblue", activebackground='black', activeforeground='red', bd=5, cursor='hand2',width=25,command=export_student)
ed.grid(row=6, column=0, padx=30,pady=10)

ex = Button(leftframe, text="Exit", font=("Times New Roman", 10, "bold"), fg="white", bg="cornflowerblue", activebackground='black', activeforeground='red', bd=5, cursor='hand2',width=25,command=exit)
ex.grid(row=7, column=0, padx=30,pady=10)

rightframe = Frame(display, bg="white")
rightframe.place(x=450, y=100, height=500, width=780)

Scrollbarx = Scrollbar(rightframe, orient=HORIZONTAL)
Scrollbary = Scrollbar(rightframe, orient=VERTICAL)

st_table=ttk.Treeview(rightframe, columns=("ID","Name","Address","Email","Passward"), show="headings", height=16,xscrollcommand=Scrollbarx.set,yscrollcommand=Scrollbary.set)
Scrollbarx.config(command=st_table.xview)
Scrollbary.config(command=st_table.yview)
Scrollbarx.pack(side=BOTTOM, fill=X)
Scrollbary.pack(side=RIGHT, fill=Y)
st_table.pack(fill=BOTH, expand=1)


st_table.config(show="headings")
st_table.heading("ID", text="ID")
st_table.heading("Name", text="Name")
st_table.heading("Address", text="Address")
st_table.heading("Email", text="Email")
st_table.heading("Passward", text="Passward")



display.mainloop()