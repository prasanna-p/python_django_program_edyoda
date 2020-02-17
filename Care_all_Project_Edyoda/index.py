from db import *
from profile import User
from younger_profile import YoungerProfile
from elder_profile import ElderProfile

# welcome note and giving oprion to login or register
def welcome():
    print("Please select\n1. Login as Elder \n2. Login as Younger\n3. Register\n4. View all youngers who are taking care\n5. View who is taking care of older couple\n6. Exit")
    task = int(input())
    if task==1:
        mobile = input("Welcome Elder\nEnter Your Email: ")
        password = input("Enter Your Password: ")
        user = ElderProfile(mobile, password)
        user.elder_log_in()
    
    elif task==2:
        mobile = input("Welcome younger\nEnter Your Email: ")
        password = input("Enter Your Password: ")
        user = YoungerProfile(mobile, password)
        user.younger_log_in()
    
    elif task==3:
        name = input("Register Yourself\nEnter Your Full Name: ")
        email = input("Enter your email: ")
        mobile = input("Enter Your Mobile Number: ")
        password = input("Enter Your Password: ")
        
        # if a user select wrong option it will ask again to select option
        while True:
            role = int(input("select your role:\n1. Elder\n2. Younger\n"))
            try:
                if role==1:
                    role="elder"
                    break
                elif role==2:
                    role="younger"
                    break
            except:
                print(f'option not Valid! Please try again')

        user_signup = User(name.lower(), email, password, mobile, role)
        user_signup.user_registration()
        print("\n\n")
        welcome()
        
    # display name of youngers who are taking care of
    elif task==4:
        sql = f'SELECT * FROM users,youngers where PK_user_id = FK_user_id'
        mycursor.execute(sql)
        younger_info = mycursor.fetchall()
        print("{:25} {:25} {:15} {:5}".format("name","Email","Contact","Rating"))
        for younger in younger_info:
            print("{:25} {:25} {:15} {}".format(younger[1],younger[2],younger[4],younger[7]))
        print("\n\n")
        welcome()

    # enter elder's mobile number of email boh are unique here and display their take care name
    elif task==5:
        sql = f'select a.name,a.email,a.mobile,b.name from users a,users b,elders e where a.PK_user_id = e.FK_user_id and b.name in (select name from users,youngers where PK_user_id = FK_user_id and PK_younger_id in (select FK_younger_id from elders,youngers where FK_younger_id = PK_younger_id and a.PK_user_id = elders.FK_user_id))'
        mycursor.execute(sql)
        care_info = mycursor.fetchall()
        print("{:25} {:25} {:15} {:25}".format("Elder Name","Email","Mobile","Care taker Name"))
        for care in care_info:
            print("{:25} {:25} {:15} {:25}".format(care[0],care[1],care[2],care[3]))
        print("\n\n")
        welcome()

    elif task==6:
        exit()

welcome()