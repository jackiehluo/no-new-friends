# No New Friends

No New Friends is a web app to connect strangers over coffee. Based on the idea of [Tea with Strangers](http://www.teawithstrangers.com/), it gives students at Columbia the chance to meet others outside of their circles who share their interests.

## App Structure
```
|-- config.py
|-- db_create.py
|-- db_downgrade.py
|-- db_migrate.py
|-- db_upgrade.py
|-- README.md
|-- run.py
|-- app/
    \
    |-- __init__.py
    |-- decorators.py
    |-- email.py
    |-- models.py
    |-- token.py
    |-- main/
    	\
    	|-- __init__.py
    	|-- views.py
    |-- static/ (CSS and JS files for styling)
    |-- templates/ (HTML templates for views)
    |-- user
    	\
    	|-- __init__.py
    	|-- forms.py
    	|-- views.py
```

### Home
![no-new-friends](https://cloud.githubusercontent.com/assets/8452682/7536181/872253d0-f55b-11e4-94cd-5fa3d72d1a3f.png)

### User Profile
![profile](https://cloud.githubusercontent.com/assets/8452682/7536182/8aa57820-f55b-11e4-9c52-53b0e753889c.png)