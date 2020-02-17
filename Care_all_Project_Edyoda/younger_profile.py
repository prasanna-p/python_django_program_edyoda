from db import *
import sys

class YoungerProfile():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        sql = f'SELECT PK_user_id, name FROM users WHERE email = "{self.email}" '
        mycursor.execute(sql)
        user_id = mycursor.fetchone()
        self.user_id = user_id[0]
        self.younger_name = user_id[1]
        sql = f'SELECT PK_younger_id FROM youngers WHERE FK_user_id={self.user_id}'
        mycursor.execute(sql)
        younger_id = mycursor.fetchone()
        self.younger_id=younger_id[0]
        sql = f'SELECT FK_younger_id from elders where FK_younger_id = {self.younger_id}'
        mycursor.execute(sql)
        self.youngerCount = mycursor.fetchall()
        sql = f'SELECT PK_user_id,name from users,elders where FK_younger_id = {self.younger_id} and PK_user_id = FK_user_id'
        mycursor.execute(sql)
        self.elder_list = mycursor.fetchall()
    
    def request_info(self):
        sql = f'select * from request'
        mycursor.execute(sql)
        return mycursor.fetchall()

    def younger_log_in(self):
        #retrieving passwords for registered mobile no from both table
        sql = f'SELECT password FROM users WHERE email= "{self.email}" '
        mycursor.execute(sql)
        user_info = mycursor.fetchone()     # fetchall provides empty list if record does not exists
        if user_info==[]:
            print(f'{self.email} ot registered. Please try to register first')
            import index      # due to mutual importing we are importing here just before method calling
        elif self.password==user_info[0]:
            print("Logged IN")
            self.dashboard_younger()
        else:
            print("Wrong email and password")
            import index

    def dashboard_younger(self):
        elderCount = len(self.youngerCount)
        print(f'Currentlty you are taking care of {elderCount} Elders\nYou can request for {4-elderCount} more elders to take care of.\n1.View list of Available elders to take care of.\n2.Give review and rating for a elder\n3.LogOut')
        choice = int(input())
        if choice==1:
            self.request_elder()
            self.dashboard_younger()
        elif choice==2:
            self.review()
            self.dashboard_younger()
        elif choice==3:
            self.log_out()

    # user should be able to see list of available elder and sent them request. NOTE:- 1 user can't sent request to same elder twice
    def request_elder(self):
        if self.request_info():
            sql = f'select name,PK_elder_id from users,elders where PK_user_id = FK_user_id and available = { True } and PK_elder_id not in(select FK_elder_id from request where request.FK_younger_id = {self.younger_id})'
        else:
            sql = f'select name,PK_elder_id from users,elders where PK_user_id = FK_user_id and available = { True }'
        mycursor.execute(sql)
        available_info = mycursor.fetchall()
        if available_info:
            keys = [i+1 for i in range(len(available_info))]
            dic_available = dict(zip(keys,available_info))
            print("{:15} {:25}".format("Serial No","Elder Name"))
            for key,value in dic_available.items():
                print("{:15} {:25}".format(key,value[0]))
            print("\n")
            request_list = list(map(int,input("Enter the Serial no of elders sepreated by comma(1,2,3....etc) to send requests:").split(",")))
            check_serialno = [num for num in request_list if not num in keys]
            if not check_serialno:
                for i in request_list:
                    sql = "INSERT INTO request(FK_younger_id,FK_elder_id) VALUES('%s','%s')"
                    val = (self.younger_id,dic_available[i][1])
                    mycursor.execute(sql,val)
                mydb.commit()
            else:
                print("you have entered some invalid number please try again")
        
            input("press enter to continue")
            print("\n\n")
        else:
            print("Currentlty you have sent request to all elders or no elders are not available")
            input("press enter to continue")
            print("\n\n")
    # younger can give rating and rating to elders
    def review(self):
        if self.elder_list:
            print("{:15} {:25}".format("Serial No","Elder Name"))
            for elder in self.elder_list:
                print("{:15} {:25}".format(elder[0],elder[1]))

            elder_id = int(input("Enter the care seeker id whome you want to review:"))
            print("Please review your care seeker press ctrl+D to submit:")
            review = sys.stdin.read()
            rating = 999
            while (rating > 6):
                rating = float(input("Please rate you care taker out of 5"))
                if rating > 5:
                    print("invalid rating please try again")
            sql = "INSERT INTO reviews (FK_user_id,review,rating,review_by) VALUES (%s, %s, %s, %s)"
            val = (elder_id, review, rating, self.younger_name)
            mycursor.execute(sql,val)
            sql2 = f'select avg(rating) from reviews where FK_user_id = {elder_id}'
            mycursor.execute(sql2)
            average_rating = mycursor.fetchone()
            sql3 = "UPDATE elders set rating = %s where FK_user_id = %s"
            val1 = (average_rating[0],elder_id)
            mycursor.execute(sql3,val1)
            mydb.commit()
            print("you review has been updated successfully")
            input("press enter to continue") 
            print("\n\n") 
            return
        else:
            print("You dont have a care seeker yet.Please go to your request_elder tab and send request to elders")
            input("press enter to continue")
            print("\n\n")
            return

    def log_out(self):
        from index import welcome
