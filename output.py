import json, requests
from bs4 import BeautifulSoup
import re
import config
from mailUser import Receiver
from findDates import dateConverter,findNextEpisode,checkYear

class UserOutput(object):

    def __init__(self,user):
        self.address=user.email
        self.TVshows=user.series
        self.final_di={}          #final output dictionary for a user
        self.final_string=""    #final output string for a user
        

    def FindFinalOutput(self):
        allseries=self.TVshows
        if allseries[-1]==",":
            allseries=allseries[:-1]
        allShows=allseries.split(",")

        for tvseries in allShows:
            tvshow=TVSHOW(tvseries)
            tvshow.StripTVShow()
            tvshow.ApiDetails()
            if tvshow.flag2:
                tvshow.final=tvshow.ostring+" is not a tv show.It is a movie probably."
            else:
                tvshow.UseDetails()
                if tvshow.flag2:
                    tvshow.final=tvshow.ostring+":There is no such tv show.Please write the tv show name properly"
            
            self.final_di[tvshow.string]=tvshow.final
        self.findFinalString()

        #Mail to User
        #R=Receiver(self.final_string,self.address)
        #R.mailIt()


    #merging all outputs of all tv series into one string for one user
    def findFinalString(self):        
        final_li=[]  
        final_li.append("\n")                         
        for v in self.final_di:
            b=list(str(v).split(" "))
            show=""
            for s in b:
                show+=s.capitalize()
                show+=" " 

            s1="TV Series Name-"+show
            s2="Status-"+str(self.final_di[v])
            final_li.append(s1)
            final_li.append("\n")
            final_li.append(s2)
            final_li.append('\n\n')
        
        final_li="".join(final_li)
        print(final_li)
        final_li = final_li.encode('utf-8')
        
            





##########################################################################################
class TVSHOW():

    def __init__(self,value):
        self.tvseries=value #name of tv show
        self.ostring=""     #original tv show string
        self.string=""      #final tv show string
        self.ID=""          #tv show id
        self.Year=""        #year
        self.TS=0           #total seasons
        self.flag=False
        self.flag2=False
        self.final=""       #final output for a particular tv show


    def StripTVShow(self):
        #stripped original string
        for ch in self.tvseries:
            ch=ch.lower()
            if (ord(ch)>96 and ord(ch)<123) or(len(self.ostring)>=0):
                self.ostring+=ch
        #all possible strings of series
        url="https://www.imdb.com/find?ref_=nv_sr_fn&q="+self.ostring+"&s=all"
        r=requests.get(url)
        soup=BeautifulSoup(r.text,"html.parser")
        try:
            s1=soup.find('table',{'class':"findList"})
            a=s1.find('td',{'class':'result_text'}).find('a')
            for t in a:
                self.string=t
        except:
            print("Please enter only a tv show")

        #print(self.string,self.ostring) #before finalising tv series




    def ApiDetails(self):
        url1 = "http://www.omdbapi.com/?apikey=d77c7587&type=series&t="+self.string       
        c=0
        r1 = requests.get(url1)
        di = json.loads(r1.text) #get json   
        try:
            self.ID=di["imdbID"] #extract tv show id
            self.Year=di["Year"] #extract year
            tS=di["totalSeasons"] #total Seasons
            if len(self.Year)==4: #it could or could not be a tv show
                if int(tS)>=1:#it is a tv show
                    self.flag=True #the show started and ended in the same year
                    c=0
                else:#not a tv show
                    c+=1
            else: # it is definitely a tv show
                c=0
        except:
            c+=1
        
        if c==1:
            c=self.findID(c)
        
        
        if c>=2:#it is definitely not a tv show
            self.flag2=True
        #print(self.string,self.ostring,c)



    def findID(self,c):
        url="http://www.omdbapi.com/?apikey=d77c7587&type=series&t="+self.ostring
        r1 = requests.get(url)
        di = json.loads(r1.text) #get json   
        try:
            Id=di["imdbID"] #extract tv show id
            Y=di["Year"] #extract year
            tS=di["totalSeasons"]
            self.ID=Id
            self.Year=Y
            self.string=self.ostring
            if len(self.Year)==4: #it could or could not be a tv show
                if int(tS)>=1:#it is a tv show
                    self.flag=True #the show started and ended in the same year
                    c=0
                else:#not a tv show
                    c+=1
            else: # it is definitely a tv show
                c=0
        except:
            c+=1

        return c



    def UseDetails(self):
        ################### CASE 1 #####################
        if len(self.Year)==9 and checkYear(self.Year):
            self.final="The show has finished streaming all its episodes."
        elif self.flag:
            self.final="The show has finished streaming all its episodes."
        ################# Other CASES ########################
        else:           
            url="https://www.imdb.com/title/"+self.ID+"/?ref_=ttep_ep_tt"
            r=requests.get(url)
            soup=BeautifulSoup(r.text,"html.parser")
            #extracting season
            try:
                s1=soup.find('div',{'class':"seasons-and-year-nav"})
                a=s1.find('a')
                for t in a:
                    self.TS=t
            except:
                self.flag2=True
            self.extractEpisodes()






    def extractAirDates(self,soup,check,epli):
        s=soup.find_all('div',{'class':'airdate'})
        for tag in s:
            for ep in tag:
                e=re.sub('[^A-Za-z0-9]+', '', ep)
                if len(e)<=4:#only year is there
                    check+=1
                    ep=e
                elif len(e)==7:#only month and year mentioned
                    ep=e
                epli.append(ep)
        
        return [epli,check]


    def nextEpisodeDate(self,epli,check):
        flag1=False
        l=len(epli)
        if check==l:#all episodes have only year mentioned
            for j in range(l):
                if epli[j] is not "":
                    ans=epli[j]
                    break
            self.final="The next season begins in:"+str(ans)+"."
        else:
            for j in range(0,l-check):#some episodes have only year mentioned
                epli[j]=dateConverter(epli[j])
                if findNextEpisode(epli[j]):
                    flag1=True
                    ans=epli[j]
                    break
            if flag1:#if next episode found
                self.final="The next episode airs on:"+str(ans)+"."
            else:#next episode not found
                for j in range(l-1,-1,-1):
                    if epli[j] is not "":
                        ans=epli[j]
                        break
                self.final="The previous episode of series was aired on->"+str(ans) \
                            +".There is no information about next season or next episode."


    #finding air date of next episode
    def extractEpisodes(self):
        n=self.TS   #total seasons
        n=int(n)
        print(self.ostring +" has seasons:"+n)
        for i in range(1,n+1):
            url="https://www.imdb.com/title/"+self.ID+"/episodes?season="+str(i)+"&ref_=tt_eps_sn_"+str(i)
            r=requests.get(url)
            soup=BeautifulSoup(r.text,"html.parser")
            try:
                check=0
                epli=[]
                [epli,check]=self.extractAirDates(soup,check,epli)
                #print(epli,check)
                self.nextEpisodeDate(epli,check)                
            except:
                self.flag2=True
                print("there is no such tv show")


    


##########################################################################################

    
      