import os
import sys
import time
import pymysql as sql
import regex as re
import inspect

gVerbose = 0

# Print Line Number
def lineno():
    return inspect.currentframe().f_back.f_lineno

# Choice
def choice(db, cursor):
    choice = input("\n1. Login\n2. Registration\n3. Exit\n\n")
    if choice=="1":
        login(db, cursor)
    elif choice=="2":
        register(db, cursor)
    elif choice=="3":
        db.close() 
        exit()
    else:
        print("Enter a Valid Choice\n")

def connect_mysql():
    # SQL Parameters
    sqlsrvr = "localhost"
    sqluser = "root"
    sqlpwd = "password"
    sqldb = "fps"

    # Connecting to MySQL DataBase and initializing a cursor to fetch data
    db = sql.connect(sqlsrvr,sqluser,sqlpwd,sqldb)
    if (db) and (gVerbose):
        print("\n*** Debug ["+str(lineno())+"]:\t"+"Connected to MySQL"+"\t***\n")
    if (not db) and (gVerbose):
        print("\n*** Debug ["+str(lineno())+"]:\t"+"Connected to MySQL"+"\t***\n")
    cursor = db.cursor()
    return db,cursor

# Login
def login(db, cursor):
    print("\n--- Login ---\n")
    unamePattern = r"\A\d[A-Z]{2}\d{2}[A-Z]{2}\d{3}"
    uname = input("\nEnter Username (USN/ID) :\t")
    uname = uname.lower()
    unameMatch = re.match(unamePattern, uname, re.I)
    if(unameMatch):
        sqlquery = "SELECT uname FROM fps.login"
        if gVerbose:
            print("\n*** Debug ["+str(lineno())+"]:\t"+sqlquery+"\t***\n")
        cursor.execute(sqlquery)
        db_uname_list = []
        li = cursor.fetchall()
        for i in li:
            db_uname_list.append(i[0])
        if uname in db_uname_list:
            pwd = input("Enter Password :\t")
            sqlquery = "SELECT password FROM fps.login where uname =\""+str(uname)+"\";"
            if gVerbose:
                print("\n*** Debug ["+str(lineno())+"]:\t"+sqlquery+"\t***\n")
            cursor.execute(sqlquery)
            dbpwd = cursor.fetchone()
            if pwd == dbpwd[0]:
                time.sleep(1)
                print("\n>> Login Successful\n")
                view_fees(db, cursor, uname)
            else:
                time.sleep(1)
                print("\n>> Password Incorrect\n")
                login(db, cursor)
        else:
            time.sleep(1)
            reg = input("\n>> USN/ID has not been registered before. Would you like register now? (y/n)\t")
            if reg.lower() in ['y','yes']:
                register(db, cursor)
    else:
        print("Error: Invalid Username\n")

def register(db, cursor):
    print("\n--- Registration ---\n")
    unamePattern = r"\A\d[A-Z]{2}\d{2}[A-Z]{2}\d{3}"
    uname = input("Enter Username (USN/ID) :\t")
    uname = uname.lower()
    unameMatch = re.match(unamePattern, uname, re.I)
    if(unameMatch):
        sqlquery = "SELECT uname FROM fps.login"
        if gVerbose:
            print("\n*** Debug ["+str(lineno())+"]:\t"+sqlquery+"\t***\n")
        cursor.execute(sqlquery)
        dbuname = cursor.fetchall()
        if uname in str(dbuname):
            ch = input("\n>> User already Registered. Would you like to login? (y/n)")
            if ch.lower() in ['y','yes']:
                login(db, cursor)
            else:
                choice(db, cursor)
        else:        
            pwd = input("Enter New Password :\t")
            cpwd = input("Enter Password again :\t")
            if pwd!=cpwd:
                print(">> Passwords not matching. Try again\n")
                time.sleep(1)
                register(db, cursor)
            else:
                sqlquery = "INSERT INTO fps.login (uname, password) VALUES(\""+uname+"\", \""+pwd+"\");"
                if gVerbose:
                    print("\n*** Debug ["+str(lineno())+"]:\t"+sqlquery+"\t***\n")
                cursor.execute(sqlquery)
                cursor.execute("COMMIT;")
                sqlquery = "INSERT INTO fps.fees (uname, exam_fee, lab_fee, club_fee, placement_fee, stationary_fee, library_fee) VALUES(\""+uname+"\", 0, 0, 0, 0, 0, 0);"
                if gVerbose:
                    print("\n*** Debug ["+str(lineno())+"]:\t"+sqlquery+"\t***\n")
                cursor.execute(sqlquery)
                cursor.execute("COMMIT;")
                sqlquery = "SELECT password FROM fps.login where uname=\""+str(uname)+"\";"
                if gVerbose:
                    print("\n*** Debug ["+str(lineno())+"]:\t"+sqlquery+"\t***\n")
                cursor.execute(sqlquery)
                dbpwd = cursor.fetchone()
                if pwd == dbpwd[0]:
                    time.sleep(1)
                    print("\n>> Registration Successful.\n\n>> You will be redirected to login now...\n")
                    login(db, cursor)
                else:
                    time.sleep(1)
                    ch = input("\n>> Registration Unsuccessful. Try Again? (y/n)")
                    if ch.lower() in ['y','yes']:
                        register(db, cursor)
    else:
        print("Invalid USN")

def view_fees(db, cursor, uname):
    print("\n--- Current Fee status ---\n")
    sqlquery = ""
    sqlquery = "SELECT exam_fee FROM fps.fees where uname=\""+str(uname)+"\";"
    if gVerbose:
        print("\n*** Debug ["+str(lineno())+"]:\t"+sqlquery+"\t***\n")
    cursor.execute(sqlquery)
    dbfees = cursor.fetchone()
    print("\nExam Fees:", dbfees)
    sqlquery = "SELECT lab_fee FROM fps.fees where uname=\""+str(uname)+"\";"
    if gVerbose:
        print("\n*** Debug ["+str(lineno())+"]:\t"+sqlquery+"\t***\n")
    cursor.execute(sqlquery)
    dbfees = cursor.fetchone()
    print("\nLab Fees:", dbfees)
    sqlquery = "SELECT club_fee FROM fps.fees where uname=\""+str(uname)+"\";"
    if gVerbose:
        print("\n*** Debug ["+str(lineno())+"]:\t"+sqlquery+"\t***\n")
    cursor.execute(sqlquery)
    dbfees = cursor.fetchone()
    print("\nClub Fees:", dbfees)
    sqlquery = "SELECT placement_fee FROM fps.fees where uname=\""+str(uname)+"\";"
    if gVerbose:
        print("\n*** Debug ["+str(lineno())+"]:\t"+sqlquery+"\t***\n")
    cursor.execute(sqlquery)
    dbfees = cursor.fetchone()
    print("\nPlacement Fees:", dbfees)
    sqlquery = "SELECT library_fee FROM fps.fees where uname=\""+str(uname)+"\";"
    if gVerbose:
        print("\n*** Debug ["+str(lineno())+"]:\t"+sqlquery+"\t***\n")
    cursor.execute(sqlquery)
    dbfees = cursor.fetchone()
    print("\nLibrary Fees:", dbfees)
    sqlquery = "SELECT stationary_fee FROM fps.fees where uname=\""+str(uname)+"\";"
    if gVerbose:
        print("\n*** Debug ["+str(lineno())+"]:\t"+sqlquery+"\t***\n")
    cursor.execute(sqlquery)
    dbfees = cursor.fetchone()
    print("\nStationary Fees:", dbfees)
    choice(db, cursor)

if __name__ == "__main__": 
    print("\n\n-------- Welcome to Fee Payment System! --------\n")

    db,cursor = connect_mysql()
    choice(db, cursor)