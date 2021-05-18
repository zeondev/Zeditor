import requests

def update():
    with open("main.py", "w") as file:
        x = requests.get('https://raw.githubusercontent.com/zeondev/Zeditor/master/main.py')
        print(x.text)
        file.write(x.text)