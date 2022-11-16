import requests 

posturl = "https://flaskmsgboard.herokuapp.com/add_message"
deleteurl = "https://flaskmsgboard.herokuapp.com/deleteid"


def deletemessage(fromid,tillid,deleteoradd,amount,content,username,imgurl):

    str(content, username, imgurl)


    postdata = {
    "Content": content,
    "Username": username,
    "imgurl": imgurl
    }


    for y in range(amount):
        requests.post(posturl, data=postdata).text
    else:
        for n in range(fromid,tillid):
            h=str(n)
            print(h)
            deletedata = {
                "idform":h
            }   
            d = requests.post(deleteurl,data=deletedata).text
            print(d)
        
        




