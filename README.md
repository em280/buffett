# buffett

A web implementation of the Stock Market Game.

### Website

An instance of this project is running at the link below, feel free to check it out:

[buffett - Stock Market Game](https://buffett-stock-market-game.herokuapp.com/) (https://buffett-stock-market-game.herokuapp.com/)

# Application Requirements

The requirements text file has been added to the repository.

This is a file that is going to help keep record and manage package dependencies for the project.
To make use of this file you will need to navigate to the folder that contains the file "requirements.txt" with regard to this project, using the terminal.

If you are on windows, you shall make use of the Windows Command Prompt or Windows Powershell. If you are on mac then the terminal would do just fine.

### Installation

The Stock-Market-Game application requires [Python](https://www.python.org/) version 3.7.2+ to run. Pip also needs to be installed.

Use the following command to install the dependencies and devDependencies.

```sh
$ pip install -r requirements.txt
```


### Running the Application

Note: The application is compatible, and has only been tested using a [Python](https://www.python.org/) version of 3.7.2+.

You can run the application by navigating to the 'buffett' folder and using the 'python' command to start up the application:

```sh
$ cd buffett

$ python application.py
```
If you are using both python2 and python3 in your system then use the following command:
```sh
$ python3 application.py
```
You can run the application in a debug mode by executing the below command if you are running a macOS 
operating system or UNIX-like operating system:

```sh
$ export FLASK_ENV=development

$ export FLASK_APP=application.py

$ flask run

```

If you are using a Windows operating system, execute the following commands to achieve the equivalent of the above:

```sh
$ set FLASK_ENV=development

$ set FLASK_APP=application.py

$ flask run

```

