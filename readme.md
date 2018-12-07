#Car Sharing System

2018-Fall Domain Analysis and Software Design Final Team Project, Ajou University

Demo site: https://daproject.sokdak.me/

Specification
--
| Service         | Implementation           | Note  |
| --------------- |:---------------:| -------:|
| Backend | Django 2.1 (Python3) |
| Database | SQLite3 |
| Frontend | Bootstrap 3 |


How to use (set-up server)
--
Before use this service, you should set-up the environment with below
```
Get Python3 from https://python.org/ and instal
Get pip and install to your computer

commands
--------
git clone https://github.com/k3nuku/da_project_carsharing
cd da_project_carsharing && python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
```

You can now access service at http://127.0.0.1:8000/

How to use (Client setup)
--
Before use this service, you should set-up the environment with below

```
First, login with your superuser account that you created
Click the username at top right side and click the [Register Station] in dropdown menu
then logout again, and create a new user with account type you wanted

That's all for preparation.
```