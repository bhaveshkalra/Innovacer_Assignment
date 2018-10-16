import mysql.connector
import config

class UsersData():
    def __init__(self):
        self.totalUsers=0
        self.cursor=""

    #database name=db1
    def connectData(self):
        print("Connecting to database..........")
        try:
            self.db=mysql.connector.connect(
                host="localhost",
                user=config.rootUser,
                password=config.pwd,
                database="db1")
            print("Database Connected sucessfully.\n")
        except:
            print("Error occured in connecting to database...")
            print("If the database is not created, it must be created first")
        
    def addUser(self,user):
        self.cursor=self.db.cursor()
        if self.totalUsers==0:
            self.cursor.execute("Create Table Users (EmailID varchar(255) primary key,\
                                FavouriteTvShows varchar(255))")
            self.cursor.execute("Show tables")
            for tb in self.cursor:
                print(tb)
        
        newUser=RowData(user)
        newUser.executeData(self.cursor)
        
        self.totalUsers+=1  #increment users
        self.db.commit()
    
    def clearData(self):
        self.cursor.execute('Drop table users')



class RowData(object):
    def __init__(self,user):
        self.u_email=user.email
        self.u_shows=user.series

    def executeData(self,mycursor):
        sqlForm="Insert into Users (EmailID,FavouriteTvShows) values (%s,%s)"
        user=[self.u_email,self.u_shows]
        mycursor.execute(sqlForm,user)

        









