<h1 align="center">Kronus.py</h1>
<br>
<br>



<br>
<p align="center">
    <img src="./docs/kronus.png" alt="Kronus.py Logo" />
</p>

<br>



<p align="center">
  <i>Chat and learn with Kronus, your virtual assistant</i>
</p>

<p align="center">
  <a href="./CONTRIBUTING.md">Contributing</a>
  ·
  <a href="https://github.com/ZhengLinLei/Kronus.py">Github</a>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/Apache-2.0">
    <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="Kronus.py License" />
  </a>&nbsp;
  <a>
    <img src="https://img.shields.io/badge/version-1.0-brightgreen" alt="Kronus.py Version" />
  </a>
</p>

<hr>








# How to use



### 1. Clone or install repository 📁

Fir git users
```
git clone https://github.com/ZhengLinLei/TkAPI.git
```

And manual download
```
https://github.com/ZhengLinLei/TkAPI/archive/refs/heads/master.zip
```


### 2. Install the modules ⬇️

Write in your terminal
```
pip install .
```

And then python will automatically install all the modules in `setup.py`. If in some cases flash an error, you can download manually the modules from `MODULES.txt` file.


### 3. Run Application ✨

Run this command
```
python src/
```

or in some python users
```
py src/
```

If you have different versions of python you need to write the current command to run the `src` folder.







# Functions 🤖

Kronus at you services! Kronus can help you anytime you want.

Try saying:
```
Hello

Where I am

Coronavirus in China

Search China in Wikipedia

Tell me the current day

What time is it

The weather

Tell me a joke

Take a screenshot

Who's your creator

Goodnight

Open youtube.com

Bye 

Exit

Turn off

Assistant

Who are you
```

### Send an email

If you want to configurate to send emails with kronus, you must to activate the option in `email.setting.json`, and insert all the email server details.
```JSON
{
    "activated": false,
    "server": "localhost",
    "port": 587,
    "login": {
        "username": "localhost",
        "password": "localhost",
        "email": "default@localhost"
    }
}
```

Try saying:
```
Send an email
```

And then if you want to enter the text manually you can say `manually` and then Kronus will open an input to enter the text.






# Comming soon


This project it is growing, and we need your help. If you find some bugs you can tell us in Github <a href="https://github.com/ZhengLinLei/Kronus.py/issues">Issues</a> section
