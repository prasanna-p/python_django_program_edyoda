from db import *
import sys


class ElderProfile():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        sql = f'SELECT PK_user_id, name FROM users WHERE email = "{self.email}" '
        mycursor.execute(sql)
        user_id = mycursor.fetchone()
        self.user_id = user_id[0]
        self.elder_name = user_id[1]
        sql = f'SELECT PK_elder_id FROM elders WHERE FK_user_id={self.user_id}'
        mycursor.execute(sql)
        elder_id = mycursor.fetchone()
        self.elder_id=elder_id[0]

    def take_care_info(self):
        sql = f'select FK_younger_id from elders where PK_elder_id = {self.elder_id}'
        mycursor.execute(sql)
        return mycursor.fetchone()

    def elder_log_in(self):
        #retrieving passwords for registered mobile no from both table
        sql = f'SELECT password FROM users WHERE email= "{self.email}"'
        mycursor.execute(sql)
        user_info = mycursor.fetchone()     # fetchall provides empty list if record does not exists
        if user_info==[]:
            print(f'{self.email} not registered. Please try to register first')
            import index      # due to mutual importing we are importing here just before method calling
        elif self.password==user_info[0]:
            print("Logged IN")
            self.dashboard_elder()
        else:
            print("Wrong email and password")
            

    def dashboard_elder(self):
        sql = f'SELECT available FROM elders where PK_elder_id = {self.elder_id}'
        mycursor.execute(sql)
        user_info = mycursor.fetchone()
        if user_info[0]==1:
            print("You are currently Available to take care of.\n1.Fund\n2.Request\n3.LogOut")
            choice = int(input())
            if choice==1:
                self.allocate_fund()
                self.dashboard_elder()
            elif choice==2:
                self.show_request()
                self.dashboard_elder()
            elif choice==3:
                self.log_out()

        else:
            print("You are currently Unavailable to take care of.\n1.Make Available\n2.Take Care Name\n3.Give review and rating for a younger\n4.Log Out")
            choice = int(input())
            if choice==1:
                self.change_status()
                self.dashboard_elder()
            elif choice==2:
                self.take_care_name()
                self.dashboard_elder()
            elif choice==3:
                self.review()
                self.dashboard_elder()
            elif choice==4:
                self.log_out()

    # elder should be able to allocate fund
    def allocate_fund(self):
        fund = input("Enter the fund amount you want to credit")
        sql = "UPDATE elders set fund = %s where PK_elder_id = %s"
        val = (fund,self.elder_id)
        mycursor.execute(sql,val)
        mydb.commit()
        print("fund have been updated successfully")
        input("Press enter to continue:")
        print("\n\n")
        return


    # elder can change their status from available to unavailable and vice-versa
    def change_status(self):
        sql1 = f'SELECT available FROM elders where PK_elder_id = {self.elder_id}'
        mycursor.execute(sql1)
        status_info = mycursor.fetchone()
        sql2 = "UPDATE elders set available = %s where PK_elder_id = %s"
        if status_info[0]:
            val = (0,self.elder_id)
        else:
            val = (1,self.elder_id)
            sql3 = "UPDATE elders set FK_younger_id = %s where PK_elder_id = %s"
            val1 = (None,self.elder_id)
            mycursor.execute(sql3,val1)
            sql4 = "DELETE from request where FK_elder_id = %s and request_status = %s"
            val2 = (self.elder_id,True)
            mycursor.execute(sql4,val2)
        mycursor.execute(sql2,val)
        mydb.commit()
        print("Status updated successfully")
        input("Press enter to continue:")
        return

    # elder can see requests and accept whome they trus only 1 request can be accepted by elder      
    def show_request(self):
        sql = f'select name,rating from users,youngers where PK_user_id = FK_user_id and FK_user_id in(select FK_user_id from youngers,request where PK_younger_id = FK_younger_id and FK_elder_id = {self.elder_id} and request_status = { False })'
        mycursor.execute(sql)
        req_info = mycursor.fetchall()
        if req_info:
            print("You have requests from following Care takers")
            print("{:25} {:10}".format("Care taker","Rating"))
            for req_list in req_info:
                print("{:25} {}".format(req_list[0],req_list[1]))
            print("\n\n")
            name = input("Enter the name of care taker you want to accept:")
            sql = f'select PK_younger_id from users,youngers where name = "{name.lower()}" and PK_user_id = FK_user_id'
            mycursor.execute(sql)
            younger_id = mycursor.fetchone()
            if younger_id:
                self.younger_id = younger_id
                sql = "UPDATE elders set FK_younger_id = %s where PK_elder_id = %s"
                val = (younger_id[0],self.elder_id)
                mycursor.execute(sql,val)
                sql1 = "UPDATE request set request_status = %s where FK_younger_id = %s and FK_elder_id = %s"
                val = (1,younger_id[0],self.elder_id)
                mycursor.execute(sql1,val)
                mydb.commit()
                print("You have successfully accepted the request of {}".format(name))
                sql2 = "DELETE from request where FK_elder_id = %s and request_status = %s"
                val = (self.elder_id,False)
                mycursor.execute(sql2,val)
                self.change_status()
            else:
                print("invalid data Please try again")
        else:
            print("currently you dont have any requests.")
        input("Press enter to continue:")
        print("\n\n")

    # elder can see name of younger who is taking care of them
    def take_care_name(self):
        younger_id = self.take_care_info()
        if younger_id:
            print("Here is some details about the person who is taking you care!")
            sql = f'select name,email,mobile from users,youngers where PK_user_id = FK_user_id and PK_younger_id = { younger_id[0] }'
            mycursor.execute(sql)
            print("{:25} {:25} {:25}".format("Care Taker","Email","Mobile No"))
            carer_info = mycursor.fetchone()
            print("{:25} {:25} {:25}".format(carer_info[0],carer_info[1],carer_info[2]))
            input("press enter to continue") 
            print("\n\n")
            return
        else:
            print("You dont have a care taker yet.Please go to your request list and accept one care taker for you")
            input("press enter to continue")
            print("\n\n")
            return
    # elder can give review and rating to youngers
    def review(self):
        younger_id = self.take_care_info()
        user = f'select FK_user_id from youngers where PK_younger_id = {younger_id[0]}'
        mycursor.execute(user)
        user_id = mycursor.fetchone()
        print("Please review your care taker press ctrl+D to submit:")
        review = sys.stdin.read()
        print("/n")
        rating = 999
        while (rating > 6):
            rating = float(input("Please rate you care taker out of 5:"))
            if rating > 5:
                print("invalid rating please try again")
        sql = "INSERT INTO reviews (FK_user_id,review,rating,review_by) VALUES (%s, %s, %s, %s)"
        val = (user_id[0], review, rating, self.elder_name)
        mycursor.execute(sql,val)
        sql2 = f'select avg(rating) from reviews where FK_user_id = {user_id[0]}'
        mycursor.execute(sql2)
        average_rating = mycursor.fetchone()
        sql3 = "UPDATE youngers set rating = %s where PK_younger_id = %s"
        val1 = (average_rating[0],younger_id[0])
        mycursor.execute(sql3,val1)
        mydb.commit()
        print("you review has been updated successfully")
        input("press enter to continue")   
        print("\n\n")
        return
        


    def log_out(self):
        from index import welcome