import vonage
import requests
import time
import threading
from flask import Flask
from flask import request
client = vonage.Client(key="cc340d08", secret="9WUpxlD4UFIIBzfr")
sms = vonage.Sms(client)

class stock(threading.Thread):

    def __init__(self): 

        threading.Thread.__init__(self) 

        self.symbol = 'null' 

        self.price = -1
    

        # helper function to execute the threads
    def set_symbol(self,newsymbol):
        self.symbol=newsymbol
    def set_price(self,newprice):
        self.price=newprice
    def get_symbol(self):
        return self.symbol
    def get_price(self):
        return self.price

    def run(self): 






        headers = {
        "X-RapidAPI-Key": "72fa973690msh297b345aca2c3d2p13befdjsnb9770d2b76a3",
        "X-RapidAPI-Host": "realstonks.p.rapidapi.com"
        }

        while True:

            if self.symbol=='null' or self.price == -1:
                time.sleep(1)
            else:
                x=str('https://realstonks.p.rapidapi.com/'+self.symbol)
                url = x

                response = requests.get(url, headers=headers)

                if response.json() == 'Invalid Stock Ticker':
                        html = ''
                        html += '<html>\n'#hmtl tag
                        html += '<body>\n'#body tag
                        html += '<p>incorrect stock string!</p>'
                        html += '<p>\n</p>'
                        html += '</body>\n'
                        html += '</html>\n'

                data=response.json()
                price=data.get('price', 0)
                if price >= self.price:
                    price=str(price)
                    textstr="The stock value is "+price+"$ and it is higher to or equal to the target price"
                    responseData = sms.send_message(
                    
                    {
                        "from": "12019031771",
                        "to": "19255779137",
                        "text": textstr,
                    }
                    )

                    if responseData["messages"][0]["status"] == "0":
                        print("Message sent successfully.")
                    else:
                        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
                    break
                else:
                    time.sleep(300)



app = Flask(__name__)
app.debug = True
thread1=stock()
thread1.start()
@app.route('/')
def form_example():
    html = ''
    html += '<body>\n'

    if thread1.get_symbol() != 'null':
        html+='<p> the stock you are monitering is '+thread1.get_symbol()+'</p>'
    html += '<form method="POST" action="/form_input">\n'#set up input
    html += 'Stock: <input type="text" name="stock" />\n'
    html+= '<form action="/action_page.php">\n'
    html+= '<p>\n</p>'
    html += '<form method="POST" action="/form_input">\n'#set up input
    html += 'Target Price: <input type="text" name="targetprice" />\n'
    html += '<p>\n<p>'
    html+='<input type="submit" value="Submit">'

    html += '</body>\n'#body tag
    html += '</html>\n'
    return html







@app.route('/form_input', methods=['POST'])#process input from form input
def form_input():





    symbol=request.form.get('stock')
    price=float(request.form.get('targetprice'))

    thread1.set_symbol(symbol)
    thread1.set_price(price)
    y=str(thread1.get_symbol)
    x=str('https://realstonks.p.rapidapi.com/'+y)
    url = x
    headers = {
    "X-RapidAPI-Key": "72fa973690msh297b345aca2c3d2p13befdjsnb9770d2b76a3",
    "X-RapidAPI-Host": "realstonks.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    if response.json() == 'Invalid Stock Ticker':
            html = ''
            html += '<html>\n'#hmtl tag
            html += '<body>\n'#body tag
            html += '<p>incorrect stock string!</p>'
            html += '<p>\n</p>'
            html += '</body>\n'
            html += '</html>\n'
            return html
    else:
        html = ''
        html += '<html>\n'#hmtl tag
        html += '<body>\n'#body tag
        html += '<p>submission successful!</p>'
        html += '<p>\n</p>'
        html+='<p> the stock you are monitering is '+thread1.get_symbol()+' at ' + str(thread1.get_price())+' dollars </p>'
        html += '</body>\n'
        html += '</html>\n'
        return html


if __name__ == '__main__':

    app.run()









