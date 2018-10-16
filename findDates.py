from datetime import date
import time
from dateutil.parser import parse


def dateConverter(sample):
    if len(sample)>7:
        return (parse(sample).strftime("%Y-%m-%d"))
    elif len(sample)==7:
        r=sample[:3]+" "+sample[3:]
        return r
    else:
        return sample


def findNextEpisode(d2):
    d1=date.today()                                   #PRESENT DATE
    d1=str(d1.year)+"-"+str(d1.month)+"-"+str(d1.day)
    if len(d2)>8:
        d1=time.strptime(d1,"%Y-%m-%d")
        d2=time.strptime(d2,"%Y-%m-%d")
    else:
        d2=parse(d2).strftime("%Y-%m")
        d1=time.strptime(d1,"%Y-%m-%d")
        d2=time.strptime(d2,"%Y-%m")
    if d1<=d2:#same dates case or d2>d1
        return True
    else:
        return False


def checkYear(y):#checking for finished series
    y=y[-4:]
    d=date.today()
    y1=str(d.year) #present year
    y1=time.strptime(y1,"%Y")
    y=time.strptime(y,"%Y")
    if y<y1:
        return True
    else:
        return False