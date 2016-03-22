# Assignment:           Mini Project 1
# Due Date:             October, 27 2015
# Name:                 Lane Scobie, Dylan Waters, Jason Yuen
# Unix ID:              scobie, dwaters, jjyuen1
# StudentID:            1448158, 1343144, 1267071
# Lecture Section:      B1
# Instructor:           Davood Rafiei
# Group:                20
#---------------------------------------------------------------
# 
#
#---------------------------------------------------------------
# library import
import sys
import datetime
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it
import random

# Sign in to use airline options.
# Must either already have login access, or create a new user.
def signIn():
    print()
    print("To continue please choose one of the following options:")
    boots= True
    
    # prompts user with options 
    while boots:
        user = input("Press 1 to login: \nPress 2 to sign-up: \nPress 3 for exit: \n")
            
        if (user=='3'):
            print("Goodbye")
            exit()
            
        elif (user== '1'):
            count=0
        
            while (count<3):               
                email= input("Enter email: ")
                email ='{0: <20}'.format(email)
                passw = getpass.getpass()
                passw = '{0: <4}'.format(passw)
                                                      
                select = "SELECT email FROM users WHERE email=:email and pass=:passw"
                curs.execute(select,{'email':email, 'passw':passw})               
                
                rows = curs.fetchall()
                
                if len(rows)>0:
                    print ("\nLogin successful for", email, "\n")                    
                    select= "SELECT name FROM airline_agents WHERE email= :email"         
                    curs.execute(select, {'email':email})
                    row1 = curs.fetchall()
                    if len(row1)>0:
                        agentName=row1[0][0]
                        # checks agents                        
                        print("Welcome Airline Agent", agentName )
                        caller(email, True)
                        count = 3
                    else:
                        caller(email, False) # So it can go back to log in screen after log out
                        count = 3           
            
                else: 
                    count+=1
                    print("Login Failed. Remaining attempts: ", 3 - count)
                    
         
        elif (user== '2'):
            print("Creating new user\n")
            validEmail = False
            while not validEmail:
                email= input("Please enter in a valid email: ")
                email ='{0: <20}'.format(email)
                select = "SELECT email FROM users WHERE email= :email"
                curs.execute(select,{'email':email})
                
                rows=curs.fetchall()
               
                if len(rows)>0:
                        print("Email taken")
                        validEmail= False
                else:
                    validEmail = True
                    
            if validEmail:
                notvalid= True
                while notvalid:
                    passw= input("Please submit a password: ")
                    if len(passw)>4:
                        print("Passwords must be only 4 characters")
                    else:
                        notvalid=False
                notvalid=True
                while notvalid:
                    name= input("Name: ")   
                    if len(passw)>20:
                        print("Name must be less than 20 characters")
                    else:
                        notvalid=False
            #have to check if email is still valid
            good = True
            select = "SELECT email FROM users WHERE email= :email"
            curs.execute(select,{'email':email})
            row = curs.fetchall()
            if len(row)>0:
                good = False
                
            if good:
                #update the tables
                insert = "insert into users values (:email, :passw, NULL)"
                curs.execute(insert,{'email':email,'passw':passw})
                
                connection.commit()
                print("New User created. Welcome", email)
               
              
            # anyother user input is invalid
            else: 
                print("Invalid input")
                boots= True
        
# This function searchs for a flight from a desired destination and availble flights
def search():
    f=open("mini-view.sql")
    full=f.read()
    comm=full.split(';')
    try:
        curs.execute('drop view available_flights')       
    except:
        pass
    finally:
        curs.execute(comm[1])
        connection.commit()
        good=False
        curs.execute('select * from airports')
        rows= curs.fetchall()
        while not good:
            src=input("Please enter the source:")
            src= src.upper()
            for row in rows:
                if src.upper() in row:
                    good=True
                    print("Departing from: "+src)
                    break
            if not good:
                for row in rows:
                    if src.upper() in row[1].upper():
                        print("Did you mean?",row[0],row[1])
                    elif src.upper() in row[2].upper():
                        print("Did you mean?",row[0],row[1])
                    elif src.upper() in row[3].upper():
                        print("Did you mean?",row[0],row[1])      
    
        curs.execute("SELECT * from airports")
        rows=curs.fetchall()
        good=False
        while not good:
            dst=input("Please enter the destination:")
            dst=dst.upper()
            for row in rows:
                if dst.upper()==row[0]:
                    good=True
                    print("Arriving at: "+dst)
                    break
            if not good:
                for row in rows:
                    if dst.upper() in row[1].upper():
                        print("Did you mean?",row[0],row[1])
                    elif dst.upper() in row[2].upper():
                        print("Did you mean?",row[0],row[1])
                    elif dst.upper() in row[3].upper():
                        print("Did you mean?",row[0],row[1])    

        good=False
        while not good:

            curs.prepare("select dep_date from sch_flights where dep_date=:datez")
        
            date=input("Please enter the departure date(DD-Mon-YYYY):")
            
            try:
                curs.execute(None, {"datez":date})
                rows = curs.fetchall()
            except:
                print("Invaild date")
            else:
                if rows==None:
                    print("No flights match that date, please try again")
                    print("Format should be (DD-Mon-YYYY), ei:22-Sep-2015")
                else:
                    good=True   

        curs.prepare("select src, dst, flightno,to_char(dep_time,'HH24:MI'), to_char(arr_time, 'HH24:MI'), fare, seats, price  from available_flights where dep_date=:datez")
        curs.execute(None, {"datez":date})
        rows=curs.fetchall()
        direct=[]
        indirSRC=[]
        indirDST=[]
        for row in rows:
            if row[0]==src.upper() and row[1]==dst.upper():
                newdir=[row[0],row[1],row[2],'Null  ',row[3],row[4],row[5],row[6],' ',' ',0,'NONE',row[7]]
                direct.append(newdir)
            elif row[0]==src.upper():
                newdir=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]]
                indirSRC.append(newdir)
            elif row[1]==dst.upper():
                newdir=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]]
                indirDST.append(newdir) 
    
        indirect=[]
        for row in indirSRC:
            for row1 in indirDST:
                if row[1]==row1[0]:
                    price=row[7]+row1[7]
                    arz=row[4].split(":")
                    dpz=row1[3].split(":")
                    hourM=(int(dpz[0])-int(arz[0]))*60
                    Mins=(int(dpz[1])-int(arz[1]))
                    Laytime=hourM+Mins
                    newdir=[row[0],row1[1],row[2],row1[2],row[3],row1[4],row[5],row[6],row1[5],row1[6],1,Laytime,price ]
                    if dpz[0]>arz[0]:
                        indirect.append(newdir)
                    elif dpz[0]==arz[0] and dpz[1]>arz[1]:
                        indirect.append(newdir)
        masterlist=[]               
        for row in direct:
            masterlist.append(row)      
        for row in indirect:
                masterlist.append(row)
                
        if len(masterlist) == 0:
            print("\n------------No flights for given date------------\n")
            return None, None
        
        notvalid=True
        while notvalid:
            answ=input("Would you like to sort based on amount of layovers(1) or Price(2): ")
            if answ=='2':
                notvalid=False
            elif answ=='1':
                notvalid=False
            else:
                print("Invalid, Please try again")
            
        if answ=='1':
            print("Sorted by Layover")
            masterlist.sort(key=lambda x: x[12])
            masterlist.sort(key=lambda x: x[10])
        else:
            print("Sorted by Price")
            masterlist.sort(key=lambda x: x[12])
        
        print("SRC DST FNO1   FNO2   ARR   DEP   Fare  Seats Fare2 Seats2 Stops Lay Price")
        for row in masterlist:
            if row[8] != ' ':
                print(row[0],row[1],row[2],row[3],row[4],row[5],row[6],'  ',row[7],'  ',row[8],'  ',row[9],'   ',row[10],'  ',row[11],'',row[12])
            else:
                print(row[0],row[1],row[2],row[3],row[4],row[5],row[6],'  ',str(row[7]).ljust(3),'  NA    NA     0     NA ', row[12])
        return masterlist,date
    
def make(email):
    masterlist,date= search()
    invalid= True
    if date== None:
        return
    datz=date    
    while invalid:   
        ans=input("Are you booking a flight with a layover?(Y/N): ")
        if ans.upper()=="N":
            print("Direct flight")
            indirect=False  
            invalid= False
        elif ans.upper()=='Y':
            print("inDirect flight")
            indirect=True   
            invalid= False
        else:   
            print("Invalid input")
    #Check if they are a passenger
    pname= input("Please enter your name: ")
    pname= '{0: <20}'.format(pname)
    check= "select count(name) from passengers where name=:pname and email=:email" 
    curs.execute(check,{'email':email, 'pname':pname})
    count= curs.fetchall()
    if count[0][0]==0: #If passenger does not exist
        country= input("What is your country of origin?")
        #Update passenger table
        insert= "insert into passengers values (:email,:pname,:country)"
        curs.execute(insert,{'email':email, 'pname':pname,'country':country})  
        connection.commit()    
    valid= False
    while not valid:
        fno1=input("Please enter the flightno: ")    
        fare1=input("Please enter the desired fare type: ")
        fare1= fare1.upper()
        fno1 ='{0: <6}'.format(fno1)    
        fare1 ='{0: <2}'.format(fare1)        
    
        for row in masterlist:
            if fno1==row[2] and fare1== row[6] and row[7]!=0:
                valid= True
            
    
    
    tjbooker(fno1,fare1,email,datz,pname)
    
    if indirect:
        valid = False
        while not valid:
            fno2=input("Please enter the 2nd flightno: ")
            fare2=input("Please enter the desired fare type: ")
            fare2= fare2.upper()            
            fno2 ='{0: <6}'.format(fno2)
            fare2 ='{0: <2}'.format(fare2)    
        
            for row in masterlist:
                if fno2==row[3] and fare2== row[8] and row[9]!=0:
                    valid= True        
        
        tjbooker(fno2,fare2,email,datz,pname)

            
def tjbooker(fno,fare,email,datz,pname):
    check= "select limit from flight_fares where flightno= '%s'"%(fno)
    curs.execute(check)
    limit= curs.fetchall()
    if limit== 0:
        print("Error: flight is full")
        return
    
    
    #Generate random ticket#
    ticket= ticket_gen()
    print('Your ticket number is: ', ticket)
    #Get/Generate seat
    seat= seat_gen()
    
    get= 'select price from flight_fares where flightno= :fno and fare= :fare'
    curs.execute(get,{'fno':fno, 'fare':fare})
    price= curs.fetchall()
    price= price[0][0]
    
    insert= "insert into tickets values (:ticket,:pname,:email,:price)"
    curs.execute(insert, {'ticket':ticket, 'pname':pname,'email':email,'price':price})
    connection.commit()        
    
    insert= "insert into bookings values (:ticket,:fno,:fare, to_date(:datz,'DD-Mon-YYYY'),:seat)" 
    curs.execute(insert, {'ticket':ticket, 'fno':fno,'fare':fare,'datz':datz,'seat':seat})
    connection.commit()

        
#Generate random ticket#
def ticket_gen():
    valid = False    
    while not valid:
        ticket= random.randint(0,999)
        select= "select count(tno) from bookings where tno= '%d'" %(ticket)
        curs.execute(select)
        count= curs.fetchall()
        if count[0][0]==0:
            valid= True    
    return ticket     
    
#Generate random seat    
def seat_gen():
    valid = False
    while not valid:
        #Generate random seat
        seats='ABCDEF'
        seatn= random.randint(1,20)
        x= random.randint(0,5)
        seat2= seats[x]
        seat= str(seatn)+str(seat2)
        select= "select count(tno) from bookings where seat= '%s'" %(seat)
        curs.execute(select)
        count= curs.fetchall()
        if count[0][0]==0:
            print('Seat is booked')
            valid= True        
   
    return seat

def list(email):
    select=("Select b.tno, t.name, b.dep_date, t.paid_price from bookings b, tickets t where b.tno=t.tno and t.email= :email order by row_number() over(order by b.tno)")
    curs.execute(select,{'email':email})
    rows=curs.fetchall()

    if len(rows)==0:
        ret=0
        print("You do not have any bookings")
    
    else:
        ret=1
        print("Ticket #:", "\t Name:", "\t\t Dept Date:", "\t\t Price:")
        for row in rows:
            print(str(row[0]).ljust(7), "\t", (row[1].strip()).ljust(8),"\t", row[2],"\t", row[3])    
            
    more= input("Would you like more information on a booking? (Y/N)")
    more= more.upper()
    if more== 'Y':   
        valid= False
        while not valid:
            try:
                which= int(input("Which booking would you like more info on?(Ticket)"))
                much= "select * from bookings where tno= '%d'" %(which)
                curs.execute(much)
                row= curs.fetchall()
                print("tno flightno  fare   date                Seat ")
                print(row[0][0],'',row[0][1],'  ',row[0][2],'   ',row[0][3],row[0][4])                
            except:
                valid= True
                print("-------------Invalid tno--------------------")
            else:
                valid= True

                
    return ret
    
def cancel(email):
    if list(email)==0:
        pass

    else:        
        check= True
        while check:
            cancel= input("Which booking would you like to cancel? Input ticket number: ")
            cancel ='{0: <20}'.format(cancel)
            try:
                select = "SELECT tno FROM bookings WHERE tno= :cancel"
                curs.execute(select,{'cancel':cancel})
            except:
                print("Invalid input")
            else:                            
                rows=curs.fetchall()
                
                if len(rows)>0:
                    print("Deleting booking for flight", cancel)
                    check= False
                    #Delete booking
                    delete = "delete from bookings where tno = '%s'" %(cancel)
                    curs.execute(delete)
                    
                    delete2 = "delete from tickets where tno = '%s'" %(cancel)
                    curs.execute(delete2)
                    
                    connection.commit()
                    print("Booking deleted\n")
                else:
                    print(cancel)
                    print("Invalid ticket number")
                
# Updates the departure time of a user inputed flight number with the current time
def updateD():
    valid = True
    while valid:
        flightno=input("---What flight number would you like to update the departure time for?\n")       
    
        update = "update sch_flights set act_dep_time = SYSDATE where flightno = '%s'" %(flightno)
        
        # Error handling to ensure flight is a flight that has left
        try:
            curs.execute(update)
            connection.commit()
            check = "select * from sch_flights where flightno = '%s'" %(flightno)
            curs.execute(check)
            newUpdate = curs.fetchall()
            print("---Flight", flightno,"to",newUpdate[0][2])
            print("---Updated flight departure time. Safe flight!\n")
            valid = False            
        except:
            print("---Invalid flight number.")
    return

# Updates the arrival time of a user inputed flight number with the current time
def updateA():
    valid = True
    while valid:
        flightno=input("---What flight number would you like to update the arrival time for?\n")       
    
        update = "update sch_flights set act_arr_time = SYSDATE where flightno = '%s'" %(flightno)
        
        try:
            curs.execute(update)
            connection.commit()
            check = "select * from sch_flights where flightno = '%s'" %(flightno)
            curs.execute(check)
            newUpdate = curs.fetchall()
            print("---Flight", flightno,"to",newUpdate[0][1])
            print("---Updated flight arrival time. Happy landing!\n")
            valid = False            
        except:
            print("---Invalid flight number.")
                              
    return   

def caller(email, agent):
    scoots= True
    while scoots:
        print("-----------------------------------------")
        print("What would you like to do?")
        do = input("Type 1 to search for flights\nType 2 to make a booking\nType 3 to list your current bookings\nType 4 to cancel a booking\nType 5 for Airline Agent options\nType 6 to logout\n------>")
        if (do== '1'):
            search()

        elif (do== '2'):
            make(email)


        elif (do=='3'):
            list(email)

        elif (do== '4'):
            cancel(email)

        elif (do == '5'):
            if agent:
                agentInput = input("---Type 1 to update departure time by flight\n---Type 2 to update arrival time by flight\n---Type 3 to go back\n")
                if agentInput == '1':
                    updateD()
                elif agentInput == '2':
                    updateA()
                
            else:
                print("You do not have suffient access.")

        elif (do== '6'):
            update = "update users set last_login = SYSDATE where email = :email"            
            curs.execute(update,{'email':email})            
            connection.commit()            
            print("Logout successful")
            connection.commit()
            scoots= False  
            
            return
        
            
        else:
            print("Invalid input")
    

if __name__ == "__main__":
    
    # Start program
    print("\n----------Welcome to AirRafiei----------")
    print("Please provide your SQL login to continue:")
    
    # get username
    user = input("Username [%s]: " % getpass.getuser())
    if not user:
        user=getpass.getuser()
            
    # get password
    pw = getpass.getpass()
    # The URL we are connnecting to
    conString=''+user+'/' + pw +'@gwynne.cs.ualberta.ca:1521/CRS'
    
    try:    
    
        # Establish a connection in Python
        connection = cx_Oracle.connect(conString)
        # create a cursor 
        curs = connection.cursor()
        
    # Login to SQL failed    
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print("Oracle code:", error.code)
        print("Oracle message:", error.message)
        print( "Login Failed. Goodbye.")
        sys.exit()
    
    signIn() 