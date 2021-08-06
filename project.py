#Student Management System
#GUI--> tkinter
#Database-->Oracle
#Run SQL Command Line -->conn-->username->system password-->panda
#create table student(rno integer primary key,name varchar(200));
#select * from student
#root--> addFrame,viewFrame,updateFrame,deleteFrame

#IMPORT
from tkinter import*
from tkinter import messagebox
from tkinter import scrolledtext
import time
import cx_Oracle
#FOR CITY NAME
import socket
import requests

#SPLASH SCREEN
#splash=Toplevel(root)
splash=Tk()
splash.title("Student Management System")

#TO DISABLE BACK BUTTON
splash.geometry("500x400+300+200")
def fs():
	pass
splash.protocol("WM_DELETE_WINDOW",fs)

#TO DELETE THE WINDOW AUTOMATICALLY AFTER 5 SECONDS

splash.after(10000,lambda:splash.destroy())

#ONLY GIF FORMAT IS SUPPORTED
image=PhotoImage(file="im2.gif")
lblPic=Label(splash,image=image,height=200,width=480)
lblPic.pack()

#TO GET THE CITY NAME
try:
	socket.create_connection(("www.google.com",80)) #HTTP port number is 80
	print("Connected")
	#messagebox.showerror("Internet Connection","Connected to network")
	res=requests.get("https://ipinfo.io")
	data=res.json()
	city=data['city']
	cityname="City : "+str(city)
except OSError as e:
	messagebox.showerror("No internet connection","Please Check your network")
lblCity=Label(splash,text=cityname,font=('ariel',18,'bold'))
lblCity.pack(side=LEFT,padx=10)

#TO GET WEATHER INFORMATION
try:
	socket.create_connection(("www.google.com",80))
	print("You are connected")
	a1="http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2="&q="+city
	a3="&appid=APP_ID" #Enter the APP_ID
	api_address=a1+a2+a3

	res=requests.get(api_address)
	

	data=res.json()
	

	main=data['main']
	

	temp=main['temp']
	temperature="Temperature : " + str(temp)

except OSError as e:
	print(e)
	messagebox.showerror("No internet connection","Please Check your network")

lblTemp=Label(splash,text=temperature,font=('ariel',18,'bold'))
lblTemp.pack(side=RIGHT,padx=10)
splash.mainloop()

#ROOT INITIALISZING
#root=Toplevel(splash)
root=Tk()
root.title("Student Management System")
root.geometry("400x400+300+200")
root.configure(background='rosy brown')



#VIEWFRAME DEFINING
viewFrame=Toplevel(root) #to add element root
viewFrame.title("View")
viewFrame.geometry("400x400+300+200")
viewFrame.withdraw() #if we dont write this then this will open with root

st=scrolledtext.ScrolledText(viewFrame,width=30,height=10)
def f3():
	viewFrame.withdraw()
	st.delete('1.0',END)
	root.deiconify()

btnViewBack=Button(viewFrame,text="Back",command=f3,bg="light blue")
st.pack()
btnViewBack.pack()

def f4():
	viewFrame.withdraw()
	root.deiconify()
viewFrame.protocol("WM_DELETE_WINDOW",f4);

#ADDFRAME

addFrame=Toplevel(root)
addFrame.title("Add")
addFrame.geometry("400x400+300+200")
addFrame.withdraw()

lblAddRno=Label(addFrame,text="Roll Number")
#lblAddRno.config(fontsize='5')
entAddRno=Entry(addFrame,bd=5)
lblAddName=Label(addFrame,text="Name")
entAddName=Entry(addFrame,bd=5)

def f5():
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect("username/password")
		cursor=con.cursor()
		sql="insert into student values ('%d','%s')"
		rno=entAddRno.get()
		if len(rno)==0:
			messagebox.showerror("Incomplete Data","Roll Number is empty")
			entAddRno.focus()
			return
		if not rno.isdigit() or int(rno)<1:
			messagebox.showerror("Incorrect input","Roll Number should be positive digits")
			entAddRno.delete(0,END)
			entAddRno.focus()
			return
		name=entAddName.get()
		if len(name)==0:
			messagebox.showerror("Incomplete data","Name is empty")
			entAddName.focus()
			return
		if not name.isalpha():
			messagebox.showerror("Incorrect input","Name must contain only alphabets")
			entAddName.delete(0,END)
			entAddName.focus()
			return
		args=(int(rno),name)
		cursor.execute(sql % args)
		con.commit()
		msg=str(cursor.rowcount)+" rows inserted"
		messagebox.showinfo("Success ",msg)
	except cx_Oracle.DatabaseError as e:
		print("Issue ",e)
		con.rollback()
		messagebox.showerror("Failure",str(e))
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
		entAddRno.delete(0,END)
		entAddName.delete(0,END)
		entAddRno.focus()


btnAddSave=Button(addFrame,text="Save",command=f5,bg="light blue")

def f2():
	addFrame.withdraw()
	root.deiconify()
btnAddBack=Button(addFrame,text="Back",command=f2,bg="light blue")


lblAddRno.pack()
entAddRno.pack()
lblAddName.pack()
entAddName.pack()
btnAddSave.pack(pady=5)
btnAddBack.pack(pady=5)

def f1():
	root.withdraw()
	addFrame.deiconify()
	addFrame.configure(background='rosy brown')
btnAdd=Button(root,text="Add",font=('arial',20,'bold'),width=10,command=f1,bg="light blue")

#UPDATEFRAME

#DEFINING
updateFrame=Toplevel(root)
updateFrame.title("Update")
updateFrame.geometry("400x400+300+200")
updateFrame.withdraw()

#COMPONENTS
lblUpdateRno=Label(updateFrame,text="Roll Number")
entUpdateRno=Entry(updateFrame,bd=5)
lblUpdateName=Label(updateFrame,text="Name")
entUpdateName=Entry(updateFrame,bd=5)


#When you press SAVE
def f6():
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect("username/password")
		cursor=con.cursor()
		sql="update student set name='%s' where rno='%d'"
		rno=entUpdateRno.get()
		if len(rno)==0:
			messagebox.showerror("Incomplete Data","Roll Number is empty")
			entUpdateRno.focus()
			return
		if not rno.isdigit() or int(rno)<1:
			messagebox.showerror("Incorrect input","Roll Number should be positive digits")
			entUpdateRno.delete(0,END)
			entUpdateRno.focus()
			return
		name=entUpdateName.get()
		if len(name)==0:
			messagebox.showerror("Incomplete data","Name is empty")
			entUpdateName.focus()
			return
		if not name.isalpha():
			messagebox.showerror("Incorrect input","Name must contain only alphabets")
			entUpdateName.delete(0,END)
			entUpdateName.focus()
			return
		args=(name,int(rno))
		cursor.execute(sql % args)
		con.commit()
		msg=str(cursor.rowcount)+" rows updated "
		messagebox.showinfo("Success ",msg)
	except cx_Oracle.DatabaseError as e:
		print("Issue ",e)
		con.rollback()
		messagebox.showerror("Failure",str(e))
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
		entUpdateRno.delete(0,END)
		entUpdateName.delete(0,END)
		entUpdateRno.focus()

btnUpdateSave=Button(updateFrame,text="Save",command=f6,bg="light blue")

#When you press BACK
def f7():
	updateFrame.withdraw()
	root.deiconify()
btnUpdateBack=Button(updateFrame,text="Back",command=f7,bg="light blue")

lblUpdateRno.pack()
entUpdateRno.pack()
lblUpdateName.pack()
entUpdateName.pack()
btnUpdateSave.pack(pady=5)
btnUpdateBack.pack(pady=5)


#WHEN YOU PRESS CLOSE
def f8():
	updateFrame.withdraw()
	root.deiconify()
updateFrame.protocol("WM_DELETE_WINDOW",f8)


#WhenYou want to VIEW the update frame
def f9():
	root.withdraw()
	updateFrame.deiconify()
	updateFrame.configure(background='rosy brown')



#DELETE FRAME
#DEFINING
deleteFrame=Toplevel(root)
deleteFrame.title("Delete")
deleteFrame.geometry("400x400+300+200")
deleteFrame.withdraw()

#COMPONENTS
lblDeleteRno=Label(deleteFrame,text="Roll Number")
entDeleteRno=Entry(deleteFrame,bd=5)

#WHEN YOU PRESS SAVE
def f10():
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect("username/password")
		cursor=con.cursor()
		sql="delete from student where rno='%d'"
		rno=entDeleteRno.get()
		if len(rno)==0:
			messagebox.showerror("Incomplete Data","Roll Number is empty")
			entDeleteRno.focus()
			return
		if not rno.isdigit() or int(rno)<1:
			messagebox.showerror("Incorrect input","Roll Number should be positive digits")
			entDeleteRno.delete(0,END)
			entDeleteRno.focus()
			return
		args=(int(rno))
		cursor.execute(sql % args)
		con.commit()
		msg=str(cursor.rowcount)+" rows deleted"
		messagebox.showinfo("Record successfully deleted ",msg)
	except cx_Oracle.DatabaseError as e:
		print("Issue ",e)
		con.rollback()
		messagebox.showerror("Failure",str(e))
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
		entDeleteRno.delete(0,END)
		entDeleteRno.focus()
btnDeleteSave=Button(deleteFrame,text="Save",command=f10,bg="light blue")

#When you press BACK
def f11():
	deleteFrame.withdraw()
	root.deiconify()
btnDeleteBack=Button(deleteFrame,text="Back",command=f11,bg="light blue")

#PACKING
lblDeleteRno.pack()
entDeleteRno.pack()
btnDeleteSave.pack(pady=5)
btnDeleteBack.pack(pady=5)

#WHEN YOU PRESS CLOSE
def f12():
	deleteFrame.withdraw()
	root.deiconify()
deleteFrame.protocol("WM_DELETE_WINDOW",f12)


#WhenYou want to VIEW the update frame
def f13():
	root.withdraw()
	deleteFrame.deiconify()
	deleteFrame.configure(background='rosy brown')




#ViewFrame View 

def f3():
	root.withdraw()
	viewFrame.deiconify()
	viewFrame.configure(background='rosy brown')
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect("username/password")
		cursor=con.cursor()
		sql="select * from student"
		cursor.execute(sql)
		data=cursor.fetchall()
		info=""
		for i in data:
			rno=i[0]
			name=i[1]
			info=info+"Roll Number "+str(rno)+" Name "+name+"\n"
		st.insert(INSERT,info)
	except cx_Oracle.DatabaseError as e:
		print("issue",e)
		messagebox.showerror("Failure",str(e))
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()


btnView=Button(root,text="View",font=('arial',20,'bold'),width=10,command=f3,bg="light blue")

btnUpdate=Button(root,text="Update",font=('arial',20,'bold'),width=10,command=f9,bg="light blue")
btnDelete=Button(root,text="Delete",font=('arial',20,'bold'),width=10,command=f13,bg="light blue")

btnAdd.pack(pady=10)
btnView.pack(pady=10)
btnUpdate.pack(pady=10)
btnDelete.pack(pady=10)

def f4():
	addFrame.withdraw()
	root.deiconify()
addFrame.protocol("WM_DELETE_WINDOW",f4)

root.mainloop()
#splash.mainloop()
