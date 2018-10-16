from user import UserInput
from output import UserOutput
from data import UsersData

def main():
    try:
        user_email=input("Enter your email address:\n")
        user_tvshows=input("Enter all your favorite tv series:\n")
        User=UserInput(user_email,user_tvshows)
        #Enter user into database
        DataBase.addUser(User)
        #output User Details
        user_output=UserOutput(User)
        user_output.FindFinalOutput()
    except:
        print("The database table must be dropped first")



DataBase=UsersData()
DataBase.connectData()

correct="Y"
while(True):
    if __name__== "__main__":
        main()
        choice=input("Do you wish to continue and Enter data for other Users(yes/no)")
        if correct != (choice[0:1].upper()):
            print("\n\nTotal Users in DB:",DataBase.totalUsers)
            DataBase.clearData()
            exit()
        else:
            pass
        

