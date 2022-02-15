
from flask import Flask, request, make_response
from datetime import datetime, timedelta
from numpy import insert
from twilio.twiml.messaging_response import MessagingResponse
import pymongo


app = Flask(__name__)
temp={}
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mydb=client['User']
information=mydb.userinformation


@app.route("/sms", methods=['GET','POST'])
def sms_reply():
   

    messagecount = int(request.cookies.get('messagecount',0))
    messagecount += 1
    print(messagecount)

    
    msg = request.form.get('Body')


    if (request.form.get('Latitude')):
        msg=None
        msg = {
                'Latitude':request.form.get('Latitude'),
                'Longitude':request.form.get('Longitude')
               }


    twml = MessagingResponse()

    
    expires=datetime.utcnow() + timedelta(hours=1)

    if (messagecount == 1):
        twml.message('Hello Dear,\nWe are food saver\nWe supply your food to NGOs\nIf you want to get details nearby NGOs\npress: 1 \nOtherwise press 2')
        resp = make_response(str(twml))
        resp.set_cookie('messagecount',value=str(messagecount),expires=expires.strftime('%a, %d %b %Y %H:%M:%S GMT'))

    elif (messagecount == 2 and msg=='1'):
        twml.message('Please provide your Details')
        twml.message('Please enter full name or press 1 to stop the process')
        resp = make_response(str(twml))
        resp.set_cookie('messagecount',value=str(messagecount),expires=expires.strftime('%a, %d %b %Y %H:%M:%S GMT'))

    elif (messagecount == 2 and msg!='1'):
        twml.message('Thank you! End of the conversation')
        temp.clear()
        resp = make_response(str(twml))
        resp.set_cookie('messagecount',value= '0', expires=0)

    elif (messagecount == 3 and msg=='1'):
        twml.message('Thank you! End of the conversation')
        temp.clear()
        resp = make_response(str(twml))
        resp.set_cookie('messagecount',value= '0', expires=0)

    elif (messagecount == 3 and msg!='1'):
        temp['Name'] = msg
        twml.message('Please enter full address or press 1 to stop the process')
        resp = make_response(str(twml))
        resp.set_cookie('messagecount',value=str(messagecount),expires=expires.strftime('%a, %d %b %Y %H:%M:%S GMT'))


    elif (messagecount == 4 and msg=='1'):
        twml.message('Thank you! End of the conversation')
        temp.clear()
        resp = make_response(str(twml))
        resp.set_cookie('messagecount',value= '0', expires=0)

    elif (messagecount == 4 and msg !='1'):
        temp['Address'] =msg
        twml.message('Please enter your phone number or press 1 to stop the process')
        resp = make_response(str(twml))
        resp.set_cookie('messagecount',value= str(messagecount), expires=expires.strftime('%a, %d %b %Y %H:%M:%S GMT'))

    elif (messagecount == 5 and msg=='1'):
        twml.message('Thank you! End of the conversation')
        temp.clear()
        resp = make_response(str(twml))
        resp.set_cookie('messagecount',value= '0', expires=0)

    elif (messagecount == 5 and msg != '1'):
        if len(msg)!=10:
            messagecount-=1
            twml.message('Invalid Phone Number\nPlease enter 10 digits of a valid phone number')
            resp = make_response(str(twml))
        else:
            temp['Mobile'] =int(msg)
            twml.message('How many people do you have food for Enter in Numeric')
            resp = make_response(str(twml))
            resp.set_cookie('messagecount',value= str(messagecount), expires=expires.strftime('%a, %d %b %Y %H:%M:%S GMT'))
    else:
        if not msg.isnumeric():
            messagecount-=1
            twml.message('Please Enter in Numeric')
            resp = make_response(str(twml))

        else:
            temp['Quantity']=int(msg)
            information.insert_one(temp)
            twml.message('Thank you for providing your information\n some NGOs nearby you will contact to you\nEnd of the conversation')
            print(temp)
            resp = make_response(str(twml))
            resp.set_cookie('messagecount',value= '0', expires=0)
            temp.clear()
            messagecount=0

    print(msg)
    return resp

if __name__ == "__main__":
    app.run(debug=True)
