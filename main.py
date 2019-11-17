import os
import sys
import time
import pymysql as sql
import regex as re
import inspect
import datetime

gVerbose = 1
gLoggedIn = 0

# Print Line Number
def lineno():
    return inspect.currentframe().f_back.f_lineno

# Choice
def choice(db, cursor):
    global gLoggedIn
    choice = input("\n1. Login\n2. Registration\n3. Exit\n\n")
    if choice=="1":
        login(db, cursor)
    elif choice=="2":
        register(db, cursor)
    elif choice=="3":
        print("\n---- Thank You! ----\n")
        gLoggedIn = 0
        db.close()
        exit()
    else:
        print("Enter a Valid Choice\n")

def choice2(db, cursor, uname):
    global gLoggedIn
    choice = input("\n1. View Current Fee Status\n2. Pay Fees\n3. View Payments\n4. Logout\n\n")
    if choice=="1":
        view_fees(db, cursor, uname)
    elif choice=="2":
        pay_fees(db, cursor, uname)
    elif choice=="3":
        view_fees(db, cursor, uname)
    elif choice=="4":
        gLoggedIn = 0
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
    global gLoggedIn
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
                gLoggedIn = 1
                choice2(db, cursor, uname)
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
    global gLoggedIn
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
                sqlquery = "INSERT INTO fps.login (uname, password, privilege) VALUES(\""+uname+"\", \""+pwd+"\", \"student\");"
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
    global gLoggedIn
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

    sqlquery = "SELECT lab_fee FROM fps.fees where uname=\""+str(uname)+"\";"
    if gVerbose:
        print("\n*** Debug ["+str(lineno())+"]:\t"+sqlquery+"\t***\n")
    cursor.execute(sqlquery)
    dbfees = cursor.fetchone()
    print("\nLab Fees:", dbfees)

    sqlquery = "SELECT lab_fee FROM fps.fees where uname=\""+str(uname)+"\";"
    if gVerbose:
        print("\n*** Debug ["+str(lineno())+"]:\t"+sqlquery+"\t***\n")
    cursor.execute(sqlquery)
    dbfees = cursor.fetchone()
    print("\nLab Fees:", dbfees)

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
    choice2(db, cursor, uname)

def pay_fees(db, cursor, uname):
    global gLoggedIn
    if(gLoggedIn):
        print("\n--- Pay Fees ---\n")
        choice = input("\n1. Exam Fees\n2. Lab Fees\n3. Placement Fees\n4. Library Fees\n5. Stationary Fee\n6. Club Fees\n\n7.Logout\n\n")
        if choice=="1":
            print("\n--- Exam Fees ---\n")
            fee_type = "exam_fee"
        elif choice=="2":
            print("\n--- Lab Fees ---\n")
            fee_type = "lab_fee"
        elif choice=="3":
            print("\n--- Placement Fees ---\n")
            fee_type = "placement_fee"
        elif choice=="4":
            print("\n--- Library Fees ---\n")
            fee_type = "library_fee"
        elif choice=="5":
            print("\n--- Stationary Fees ---\n")
            fee_type = "stationary_fee"
        elif choice=="6":
            print("\n--- Club Fees ---\n")
            fee_type = "club_fee"
        elif choice=="7":
            gLoggedIn = 0
            db.close() 
            exit()
        
        sqlquery = "SELECT "+str(fee_type)+" FROM fps.fees where uname=\""+str(uname)+"\";"
        if gVerbose:
            print("\n*** Debug ["+str(lineno())+"]:\t"+sqlquery+"\t***\n")
        cursor.execute(sqlquery)
        dbfees = cursor.fetchone()
        print("\nCurrent Balance:", dbfees)
        amount = input("\nEnter amount to be paid:")
        while(int(amount) <= 0):
            amount = input("\nEnter valid amount:")
        card_number = input("\nEnter your Credit/Debit Card number:")
        while not(re.match(r"\d{16}",str(card_number), re.I|re.M)):
            card_number = input("\nEnter valid Credit/Debit Card number:")
        cvv = input("\nEnter your 3 digit CVV number:")
        while not(re.match(r"\d{3}",str(cvv), re.I|re.M)):
            cvv = input("\nEnter valid CVV number:")
        expiry_date = input("\nEnter expiry date of your card in the format mm/yyyy:")
        while not(re.match(r"\d{2}\/\d{4}",str(expiry_date), re.I|re.M)):
            expiry_date = input("\nEnter a valid expiry date:")
        now = str(datetime.datetime.now())
        print("\nDo Not Refresh/Cancel while the transaction is being processed\n")
        time.sleep(3)
        trans_id = now.strip()
        trans_id = trans_id.replace("-","")
        trans_id = trans_id.replace(":","")
        trans_id = trans_id.replace(".","")
        transaction_id = trans_id[::-1]
        print("\ntransaction_id: ",transaction_id)
        if gVerbose:
            print("\ntransaction_id: ",transaction_id)
        sqlquery = "INSERT INTO fps.login (uname, type, amount_to_be_paid, amount_paid, amount_left, card_number, cvv, expiry_date, time_stamp, transaction_id) VALUES(\""+uname+"\", \""+fee_type+"\", \""+dbfees+"\", \""+amount+"\", \""+(int(dbfees)-int(amount))+"\", \""+card_number+"\", \""+cvv+"\", \""+expiry_date+"\", \""+str(now)+"\", \""+transaction_id+"\");"
        if gVerbose:
            print("\n*** Debug ["+str(lineno())+"]:\t"+sqlquery+"\t***\n")
        cursor.execute(sqlquery)
        cursor.execute("COMMIT;")
        print("\n>Transaction Successful\n")
        choice2(db, cursor, uname)
    else:
        choice(db, cursor)

if __name__ == "__main__": 
    print("\n\n-------- Welcome to Fee Payment System! --------\n")

    db,cursor = connect_mysql()
    choice(db, cursor)