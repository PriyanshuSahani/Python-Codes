#Contains the list of operations performed in the current session
operations = []

#Shows the list of operations.
def queries():
    print("Query List : ")
    for i in operations:
        print(i)

#To Establish Connection
def ec(dbnm = "F2DB"):
    import mysql.connector
    global mydb
    global mycursor
    mydb = mysql.connector.connect(host = "localhost",user = "root", passwd = "root", database = dbnm)
    print(mydb)
    mycursor = mydb.cursor(buffered = True)
    print(mycursor)
    print("Database in use : ",mydb.database)
    operations.extend(["------x-------x-------x------"," ","In "+mydb.database," "])

ec()

#Create new Database
def createdb():
    x = input("Database Name - ")
    arg = "create database "+x+""
    execute(arg)
    
#Change Dtabase
def changedb():
    dbname = input("Database Name - ")
    try:
        arg = "use "+dbname+""
        execute(arg)
        ec(dbname)
    except:
        print("No such database exists")
        opt = input("Do you want to create a database by that name?(Yes/No)")
        if opt == "Yes":
            arg = "create database "+dbname+""
            execute(arg)
            arg = "use "+dbname+""
            execute(arg)
            ec(dbname)

#Shows all the tables in the current database
def tables():
    arg = "show tables"
    execute(arg)

#Creates a new table.
def createtable():
    tblnm = input("Table Name - ")
    cl = []
    tcd = {}
    cdet = ""
    def AddColumns():
        print("Enter '~!' to stop entering more columns")
        while True :
            cn = input("Column Name - ")
            if cn == "~!":
                break
            else:
                cl.append(cn)
    def Datatypes():
        print("Feed the Date Types of")
        for i in cl:
            tcd[i] = []
            print(i , end = "")
            dt = input(" - ")
            tcd[i].append(dt)
    def IndexSupport():
        for i in cl:
            print(i," : ",cl.index(i))
    def PrimaryKey():
        pri = input("Indexes of Columns to be declared as Primary Key(without seperation)\n")
        for i in pri :
            tcd[cl[int(i)]].append("primary key")
    def NotNull():
        notnull = input("Indexes of Columns to be set as Not Null type(without seperation,excluding primary keys)\n")
        for i in notnull :
            tcd[cl[int(i)]].append("not null")
    def Unique():
        uni = input("Indexes of Columns to be set as Unique(without seperation)\n")
        for i in uni :
            tcd[cl[int(i)]].append("unique")
    def SetDefault():
        sd = input("Indexes of Columns to be given a Default value\n")
        if sd != "":
            print("Enter the default values of :\n")
        for i in sd:
            tcd[cl[int(i)]].append("default")
            print(cl[int(i)],end = "")
            x = input(" - ")
            v = "'%s'"%(x)
            tcd[cl[int(i)]].append(v)
    def Convertor():
        nonlocal cdet
        x = ""
        for i in cl:
            x += i
            x += " "
            for j in tcd[i]:
                x += j + " "
            x+= ","
        cdet = x[:len(x)-2]
    
    AddColumns()
    Datatypes()
    IndexSupport()
    PrimaryKey()
    NotNull()
    Unique()
    SetDefault()
    Convertor()
    arg = "create table %s (%s)"%(tblnm,cdet)
    print(arg)
    execute(arg)

# Alter a table's structure(operation - add, modify, drop, change)
def alter(table_name,operation):
    def add(tbnm):
        n = int(input("Number of Columns - "))
        arg = "alter table "+tbnm+" add ("
        for i in range (n):
            cnm = input("Column Name - ")
            dt = input ("Data Type -")
            cnstr = input("Constraint(s) - ")
            arg = arg + cnm + " " + dt + " " +cnstr + ","
            if i  == n-1:
                arg = arg[:len(arg)-1]
        arg += ")"
        execute(arg)

    def modify(tbnm):
        cnm = input("Column Name - ")
        dt = input ("Data Type -")
        cnstr = input("Constraint(s) - ")
        arg = "alter table "+tbnm+" modify "+cnm+" "+dt+" "+cnstr
        execute(arg)

    def change(tbnm):
        cnm = input("Column Name - ")
        ncnm = input("New Name - ")
        dt = input ("Data Type -")
        cnstr = input("Constraint(s) - ")
        arg = "alter table %s change %s %s %s %s"%(tbnm,cnm,ncnm,dt,cnstr)
        execute(arg)

    def drop(tbnm):
        cnm = input("Column Name - ")
        arg = "alter table %s drop %s"%(tbnm,cnm)
        execute(arg)
    l = ["add","change","modify","drop"]
    op = [add,change,modify,drop]
    op[l.index(operation)](table_name)



#To View a Table's Structure
def desc():
    tbnm = input("Table Name - ")
    global arg
    arg = "desc %s"%(tbnm)
    execute(arg)

#Deletes a table
def droptb():
    tbnm = input("Table Name - ")
    import restb
    file = open("tbref")
    x = file.read()
    ref = x.split("\n")
    ref.reverse()
    for i in ref:
        a= i.split(",")
        if a[0] ==tbnm and a[1] == mydb.database:
            Id = a[2]
            break
    restb.cpkernel(Id)
    arg = "drop table %s"%(tbnm)
    execute(arg)
    file.close()

#Insert Rows
def insert():
    print("Enter '~!!' to terminate the process.")
    print("Enter '~!' to cancel current insertion.")
    tbnm = input("Table Name - ")
    mycursor.execute("desc %s"%(tbnm))
    msg = []
    for i in mycursor:
        msg.append(i[0]+"  -  ")
    while True:
        x = ""
        L = [0,0,0]
        for i in range(len(msg)):
            L[i] = input(msg[i])
            if L[i] == '~!':
                break
            elif L[i] == '~!!':
                x = 'exit'
                break
        else:
            global arg
            arg = "insert into %s values(%s,'%s',%s)"%(tbnm,L[0],L[1],L[2])
            operations.append(arg)
            mycursor.execute(arg)
            mydb.commit()
        if x == 'exit':
            break

#Display entire Content of a Table
def display():
    tbnm = input("Table Name - ")
    arg = "select * from "+tbnm+""
    execute(arg)

def NullConditionGenerator(tbnm):
    mycursor.execute("Desc "+tbnm+"")
    c1 = mycursor.fetchone()
    print(c1)
    cn = c1[0]
    val = "e" if "int" in c1[1] else 2
    print(val)
    return cn,val

#Display Specific Details
def select():
    tbnm = input("Table Name - ")
    cl = input("Column List (Seperated by ',')")
    cn,val = NullConditionGenerator(tbnm)
    C = ""+cn+" != '"+str(val)+"'"
    G = None
    H = 'count(*) > 0'
    print("Key: \nWhere Clause   : C \nGroup By Clause : G \nHaving Clause   : H")
    o = input("Keys of Clauses you want to Add(without seperation eg., 'CG')")
    if 'C' in o:
        C = input("Condition (Where Clause)")
    if 'G' in o:
        G = input("Group by Clause(Column Name) - ")
    if "H" in o:
        H = input("Having Clause - ")
    global arg
    if G == None:
        arg = "select %s from Books where %s"%(cl,C)
        print(arg)
    else:
        arg = "select %s from "%(cl)+tbnm+" where %s group by %s having %s"%(C,G,H)
        print(arg)
    execute(arg)


def execute(arg):
    mycursor.execute(arg)
    for x in mycursor:
        print(x)
    operations.append(arg)

#Update the Enteries in a Row
def update():
    tbnm = input("Table Name - ")
    print("Column List : ")
    mycursor.execute("desc "+tbnm+"")
    cl = []
    for x in mycursor:
        cl.append(x[0])
    print(cl)
    c = input("Column to be Updated - ")
    v = input("Value - ")
    C = input("Condition (Where Clause) - ")
    wc = "where " + C if C != "" else ""
    global arg
    arg = "update %s set %s = %s %s"%(tbnm,c,v,wc)
    print(arg)
    execute(arg)
    mydb.commit()

#Disconnects Cursor and terminates the connection with mysql
def close():
    mycursor.close()
    mydb.close()
    print("Session Ended.")