# Flask Postgres Demo

This is a simple demo to show and explain a very basic flask session authentication setup.

## 🗂 Project Overview

The project is meant to demonstrate very basic authentication and authorization with Flask.

* **app.py**: This is the main project file containing the entire logic of the app and the most relevant code.
* **requirements.txt**: A list of all installed packages and their versions
* **templates/**: All the views. The _base.html is the main layout for all pages.
* **static/**: Contains static assets. So far it's a CSS file, with some basic normalizing styles.

## 🚀 Getting started locally

### 🖥 Setting up the project environment

First, make sure to have Python 3 installed. **Mac** should come with it preinstalled. If not, you should use something like [Homebrew](https://brew.sh/) to install the latest version. On **Windows 10**, you can install the latest version of Python simply from the Microsoft Store app. For Linux, follow [the instructions here](https://docs.python-guide.org/starting/install3/linux/).

Then setup and activate your virtual environment: 

#### Linux & Mac

* Install a virtual environment to install Python packages only in your project's environment: `pip3 install virtualenv` (Depending on your Mac version and set up, you may need to run `sudo pip3 install virtualenv` to install it as an admin)
* Create an environemnt folder: `virtualenv env`
* Activate the environment: `source env/bin/activate`

Before you work on your project, make sure that it says `(env)` in your Terminal. This way you know, that you're currently working within the environment you just set up.

#### Windows 10

* Install a virtual environment to install Python packages only in your project's environment: `pip3 install virtualenv`
* Create an environemnt folder: `python -m virtualenv .`
* (Optional) Most likely, Windows won't allow you to execute the environment script. So probably you have to run the following line to temporarily grant that permission: `Set-ExecutionPolicy Unrestricted -Scope Proces`
* Now acticate the environment: `.\Script\activate`

Your Command Prompt should now show the name of your project in parentheses. Example: `(flask-auth-demo)`. This is how you know, the environment is active.

### 📦 Installing all relevant packages

Now, let's install all packages that we need: 

```sh
pip3 install -r requirements.txt
```

This will install the main three packages we need:

* `flask` (Flask framework for our application)
* `flask-sqlalchemy` (This will help us interact with our database in Python much more comfortably)
* `gunicorn` (This is the web server that will be running on Heroku)

_(Check the requirements.txt file to view the versions of the packages used for this demo.)_

As long as we have set up our environment before, all packages will be installed in the **env** folder.

### 🗄 Setup the sqlite database locally

In order to set up a database, we have to do the following steps:

1. Open the python console: `python3` (or just `python` on Windows)
2. Import the database from our project: `from app import db`
3. Create the database file: `db.create_all()`
4. Close the console: `exit()`

### 🧨 Run the server

Now, that everything is set up you can start the server:

#### Linux & Mac

```sh
python3 app.py
```

#### Windows

```sh
python app.py
```

## 🌏 Deployment on Heroku

To deploy this application to Heroku we have to prepare a few things. 

### Setting up git

We will use the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) below. It integrates nicely with git. So ideally you use git with your project to keep things easier.

If you haven't already, you should install [git](https://git-scm.com/) as version control for your application. It often comes preinstalled on your system. You can check that by running `git` in the command line. Otherwise you can just install it.

If you don't know how to use it yet, don't worry. All you need to do for now is run the following commands in your project directory: 

```sh
git init
git add .
git commit -am "initial commit"
```

### Set up your project on Heroku

#### Create Project on Heroku

1. Create an account on [Heroku](https://heroku.com)
2. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli). This will allow you to manage and deploy to your Heroku app right from the command line.
3. Now login with the CLI running: `heroku login` (follow the steps)
4. If you haven't already, navigate to your project directory within the command line and now run `heroku create`. This will create a project on Heroku for your app. Go to the dashboard on [heroku.com](https://heroku.com) and you will see it show up there. 

When creating your application the CLI returned two links and the application name. It looks something like this:

```sh
Creating app... done, ⬢ sheltered-anchorage-06094
https://sheltered-anchorage-06094.herokuapp.com/ | https://git.heroku.com/sheltered-anchorage-06094.git
```

In this example, our application name is `sheltered-anchorage-06094`

We will need those soon!

#### Prepare for deployment

There are only two small steps we need to do before we can deploy our Flask app to Heroku:

1. Tell it how to run the server
2. Set up our Postgres database on Heroku

**1) Tell it how to run the server**

Create a file in your project folder called `Procfile`. 

Add the following line to it: `web: gunicorn app:app`

That's it. This file tells Heroku to use [gunicorn](https://gunicorn.org/) (the package we installed earlier) as a web server for our application. 

**2) Set up our Postgres database on Heroku**

As a database we use Postgres. In Heroku, databases are added to your project as so called "addons". Heroku offers a free version of Postgres which we will use. 

To add the Postgres addon to your project simply replace "your-app-name-123" with your application name and run the following command:

```sh
heroku addons:create heroku-postgresql:hobby-dev --app your-app-name-123
```

(Remember, the app name you got from the CLI earlier! It probably looks something like this: `sheltered-anchorage-06094`)

Heroku will not only create a database. It now also sets an environment variable with the name of `DATABASE_URL`. You can check it out by running `heroku config --app your-app-name-123` (again with your app name instead of your-app-name-123). This command will output all currently set environment variables on Heroku.

Environment variables allow us to use different configurations on our local machine than on a server. In our situation that's helpful because we would like to use sqlite locally but Postgres on Heroku. Have a look at the app.py file and look for this code:

```python
if os.environ.get('DATABASE_URL'):
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
else:
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
```

The function `os.environ.get('DATABASE_URL')` tries to get an environment variable of the name of `DATABASE_URL`. This conditional checks if that environment variable is present. If it is, it should use that one as URL to our database (on Heorku that's the URL to Heroku). If the variable isn't set, we should just use SQlite instead.

>**Important side note:** You may have gotten confused by `.replace("://", "ql://", 1)`. That's a workaround because of an update in the sqlalchemy library and a mismatch with the way Heroku configures its Postgres database. You can read about it [here](https://stackoverflow.com/questions/66690321/flask-and-heroku-sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy).

Now, there is one last step required for Heroku to properly run Postgres with your application. You have to add `psycopg2==2.8.6` to your "requirements.txt" file. This is a package Heroku needs to run properly and without much additional set up you won't be able to install it locally.


#### Deployment (finally!)

Now that your application is set up, you can deploy to Heroku. As mentioned before, Heroku CLI uses the git workflow. So you deploy simply by running: 

```
git push heroku master
```

_or if you're using `main` you run `git push heroku main`_

(If you set up Heroku before running `git init` follow [these steps](https://devcenter.heroku.com/articles/git) to set up your Heroku remote)

The very first time you delpoy your app you have to initialize your database again the same way you did it locally before. On Heorku you do it with the following commands:

```
heroku run python
```

Now you are in the python console but on the Heroku server. Here run: 

```
from app import db
db.create_all()
exit()
```

(You will have to repeat these steps every time you change something about your database set up.)

And that's it! Your app is live on Heroku! The CLI will return a URL like this one "https://sheltered-anchorage-06094.herokuapp.com/" which is the URL of your application. You can click it and should see your application live. 
