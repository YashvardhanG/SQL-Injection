#Modules
import tkinter as tk
from tkinter import *
import ctypes
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import webbrowser  

ctypes.windll.shcore.SetProcessDpiAwareness(1)

result_array = []
form_value = -1
final_value = 0

#Inapp Input
def super():
    query.delete(0,'end')
    query.insert(0,' ')
    query.focus()

#Main Input
def enter(event):
    command =str(query.get().lower().lstrip())
    query.delete(0,'end')
    query.insert(0,' ')
    assistant(command)

#Result Pane
def result(form_value):
    text = ""
    for ele in result_array:
        text += (ele+"\n")

    if (form_value != -1):
        url= 'https://www.tek-tools.com/security/sql-injection-attack#how-to-prevent-sql-injection-attacks'  
        webbrowser.open_new_tab(url)  
        form_value = -1

    result = Toplevel(root)
    result.geometry("1000x150+"+str(int(root.winfo_screenwidth()/2)-500)+"+"+str(int(root.winfo_screenheight()/2)-310))
    result.overrideredirect(True)
    result.config(highlightbackground="#1f2127", highlightthickness = 2)
    result['bg'] = '#1f2127'
    label = tk.Label(result, bg = '#1f2127', fg='#FFFFFF', text = text, font= ('Calibri Light',13,'normal')).place(relx=.5, rely=.5, anchor= CENTER)
    result.attributes('-topmost', True)
    result_array.clear()
    result.update()

#Close event
def exit(event):
    quit()

#Close Hover In
def cross_enter(event):
    close.config(bg='red')

#Close Hover Out
def cross_leave(event):
    close.config(bg='#271c24')
        
#Close Hover In
def enter_enter(event):
    voice.config(bg='aqua')

#Close Hover Out
def enter_leave(event):
    voice.config(bg='#271c24')
        

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

def get_all_forms(url):
    soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    details = {}
    
    try:
        action = form.attrs.get("action").lower()
    except:
        action = None
    
    method = form.attrs.get("method", "get").lower()
    
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def is_vulnerable(response):
    errors = {
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
    }

    for error in errors:
        if error in response.content.decode().lower():
            return True

    return False
    
def scan_sql_injection(url):
    for c in "\"'":
        new_url = f"{url}{c}"
        result_array.append("[!] Trying" + new_url)
        res = s.get(new_url)
        if is_vulnerable(res):

            result_array.append("[+] SQL Injection vulnerability detected, link:" + new_url)
            return
    
    forms = get_all_forms(url)
    result_array.append(f"[+] Detected {len(forms)} forms on {url}.")
    global final_value 
    final_value = len(forms)

    for form in forms:
        form_details = get_form_details(form)
        for c in "\"'":
            data = {}
            for input_tag in form_details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    try:
                        data[input_tag["name"]] = input_tag["value"] + c
                    except:
                        pass
                elif input_tag["type"] != "submit":
                    data[input_tag["name"]] = f"test{c}"
            url = urljoin(url, form_details["action"])
            if form_details["method"] == "post":
                res = s.post(url, data=data)
            elif form_details["method"] == "get":
                res = s.get(url, params=data)
            if is_vulnerable(res):
                result_array.append("[+] SQL Injection vulnerability detected, link:" + url)
                result_array.append("[+] Form:")
                result_array.append(form_details)
                break

#Main Command
def assistant(command):
        #Hello
        if 'hello' in command:
            form_value = -1
            result_array.append("Hello, How are you?")
            result(form_value)

        else:
            form_value = 0
            scan_sql_injection(command)   
            result(form_value)

#Tkinter UI and Loop
root = tk.Tk()
root.bind('<Return>',enter)
root.bind('<Escape>',exit)
root.geometry("1000x43+"+str(int(root.winfo_screenwidth()/2)-500)+"+"+str(int(root.winfo_screenheight()/2)-350))
root['bg'] = '#1f2127'
root.overrideredirect(True)
root.attributes('-topmost', True)
root.update()

#Enter Button Config
voice = tk.Button(width = 4, text='->', bg='#271c24', fg='#5f595e',font=('Calibri',12,'bold'), bd=0, command = 'result')
voice.grid(row=1,column=3)
voice.bind('<Enter>', enter_enter)
voice.bind('<Leave>', enter_leave)

#Search Bar Config
query = tk.Entry(root, font=('Montserrat',12,'normal'), width = 53, bg='#1f2127', takefocus = 0, bd=0, fg='#FFFFFF', highlightbackground = "#5f595e", highlightcolor= "#5f595e", highlightthickness=1)
query.insert(0,'Enter a URL for SQL Vulnerability Analysis')
query.focus()
query.grid(row=1,column=2)

#Exit Button Config
close = tk.Button(width = 3, bg='#271c24', text='X', fg='#5f595e', font=('Calibri',12,'bold'),  bd=0, command = 'exit')
close.grid(row=1, column=1)

close.bind('<Enter>', cross_enter)
close.bind('<Leave>', cross_leave)

root.mainloop()