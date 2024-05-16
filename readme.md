# Welcome To Garden Frenzy Backend Aplication


## Description

- What your application does,
- Why you used the technologies you used,
- Some of the challenges you faced and features you hope to implement in the future.


## Setup
This setup assume you using windows, python 3.11.5 and XAMPP installed in your PC, and you have a ngrok account.

1. Create new sql database named `game_db` using XAMPP

2. Open CMD and create new Python Virtual Environtment

```
python -m venv venv
```
3. Activate the Virtual Environtment
```
venv\scripts\activate
```
4. Install the python package requirements
```
pip intall -r requirements.txt
```
5. Run flask application
```
python -m app.run
```
6. Open ngrok.exe
7. Connect the ngrok account
```
ngrok config add-authtoken <your auth token>
```
8. Port Forwarding
```
ngrok http http://localhost:5000/ --domain=<your domain>
```

