import os
import sys
import time
import pymysql as sql
import regex as re

# Login
def login(cursor):
    print("\n--- Login ---\n")
    unamePattern = r"\A\d[A-Z]{2}\d{2}[A-Z]{2}\d{3}"
    uname = input("\nEnter Username (USN/ID) :\t")
    uname = uname.lower()
    unameMatch = re.match(unamePattern, uname, re.I)
    if(unameMatch):
        sqlquery = "SELECT uname FROM fps.login"
        cursor.execute(sqlquery)
        db_uname_list = []
        li = cursor.fetchall()
        for i in li:
            db_uname_list.append(i[0])
        if uname in db_uname_list:
            pwd = input("Enter Password :\t")
            sqlquery = "SELECT password FROM fps.login where uname =\""+str(uname)+"\";"
            cursor.execute(sqlquery)
            dbpwd = cursor.fetchone()
            if pwd == dbpwd[0]:
                time.sleep(1)
                print("\n>> Login Successful\n")
                view_fees(cursor, uname)
            else:
                time.sleep(1)
                print("\n>> Password Incorrect\n")
                login(cursor)
        else:
            time.sleep(1)
            reg = input("\n>> USN/ID has not been registered before. Would you like register now? (y/n)\t")
            if reg.lower() in ['y','yes']:
                register(cursor)
    else:
        print("Error: Invalid Username\n")

def register(cursor):
    print("\n--- Registration ---\n")
    unamePattern = r"\A\d[A-Z]{2}\d{2}[A-Z]{2}\d{3}"
    uname = input("Enter Username (USN/ID) :\t")
    uname = uname.lower()
    unameMatch = re.match(unamePattern, uname, re.I)
    if(unameMatch):
        pwd = input("Enter New Password :\t")
        cpwd = input("Enter Password again :\t")
        if pwd!=cpwd:
            print(">> Passwords not matching. Try again\n")
            time.sleep(1)
            register(uname)
        else:
            sqlquery = "INSERT INTO fps.login (uname, password) VALUES(\""+uname+"\", \""+pwd+"\");"
            print("####>>>>\t",sqlquery)
            cursor.execute(sqlquery)
            cursor.execute("COMMIT;")
            sqlquery = "INSERT INTO fps.fees (uname, exam_fee, lab_fee) VALUES(\""+uname+"\", 0, 0);"
            print("####>>>>\t",sqlquery)
            cursor.execute(sqlquery)
            cursor.execute("COMMIT;")
            sqlquery = "SELECT password FROM fps.login where uname=\""+str(uname)+"\";"
            cursor.execute(sqlquery)
            dbpwd = cursor.fetchone()
            if pwd == dbpwd[0]:
                time.sleep(1)
                print("\n>> Registration Successful.\n\n>> You will be redirected to login now...\n")
                login(cursor)
            else:
                time.sleep(1)
                ch = ("\n>> Registration Unsuccessful. Try Again? (y/n)")
                if ch.lower() in ['y','yes']:
                    register(cursor)
    else:
        print("Invalid USN")

def view_fees(cursor, uname):
    print("\n--- Current Fee status ---\n")
    sqlquery = ""
    sqlquery = "SELECT exam_fee FROM fps.fees where uname=\""+str(uname)+"\";"
    cursor.execute(sqlquery)
    dbfees = cursor.fetchone()
    print("\nExam Fees:", dbfees)
    sqlquery = "SELECT lab_fee FROM fps.fees where uname=\""+str(uname)+"\";"
    cursor.execute(sqlquery)
    dbfees = cursor.fetchone()
    print("\nLab Fees:", dbfees)
    
    if (Exam Fees <0 or Lab Fees <0):

    def fees_paid(cursor, uname):
    print("\n--- fees paid ---\n")
    sqlquery = ""
    sqlquery = "SELECT Exam Fees FROM fps.fees_paid where uname=\""+str(uname)+"\";"
    cursor.execute(sqlquery)
    dbfees_paid = cursor.fetchone()
    print("\nExam Fees:", dbfees_paid)



if __name__ == "__main__": 
    print("\n\n-------- Welcome to Fee Payment System! --------\n")

    choice = input("\n1. Login\n2. Registration\n3. Exit\n\n")
    # SQL Parameters
    sqlsrvr = "localhost"
    sqluser = "root"
    sqlpwd = "password"
    sqldb = "fps"

    # Connecting to MySQL DataBase and initializing a cursor to fetch data
    db = sql.connect(sqlsrvr,sqluser,sqlpwd,sqldb)
    cursor = db.cursor()
    if choice=="1":
        login(cursor)
    elif choice=="2":
        register(cursor)
    elif choice=="3":
        exit()
    else:
        print("Enter a Valid Choice\n")
    db.close()