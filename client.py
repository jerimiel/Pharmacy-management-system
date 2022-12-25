import requests
import json
from tkinter import *
from tkinter import ttk


# details = {"name": 'paracetamol', "brand": 'emzor'}
# url = f'''http://127.0.0.1:5000/searchinfo/{json.dumps(details)}'''
# data = requests.get(url)
# response = json.loads(data.content)

# if response == []:
#     print("Not available")
# else:
#     print(response)
def pressed():
    details = {}
    details["name"] = drug.get()
    details["brand"] = None
    url = f'''http://127.0.0.1:5000/searchinfo/{json.dumps(details)}'''
    print(url)
    data = requests.get(url)
    response = json.loads(data.content)
    if response == []:
        #print("Not Available")
        output["text"] = "Not Available"
    else:
        text = ""
        for i in response:
            med = ""
            for j in i:
                med = med + str(j) + "  "
            text = text + med + "\n"
        output["text"] = text


root = Tk()

Frame = ttk.Frame(root, padding = 10)
Frame.grid()
drug = StringVar()

drug_label = Label(Frame,text = "Drug Name",foreground="Green")
drug_label.grid(row = 0,column = 0)
input_drug = Entry(Frame, width=20,background="black",foreground="green", textvariable=drug,font=20, cursor="plus #0000FF")
input_drug.grid(row = 1, column=0,ipadx=10, ipady=10)

output = Label(Frame, text="Answer here")
output.grid(row = 2, column = 0, pady=30)

button = Button(Frame, text="SEARCH", command = pressed)
button.grid()

root.mainloop()

