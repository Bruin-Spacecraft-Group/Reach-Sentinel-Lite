# Reach-Sentinel-Lite


## Quick start

1. First, you must download the following:
	 - download Django from the Django website, ideally for python-3: https://www.djangoproject.com/
	 - pip install the packages: 'pyserial, requests, and numpy' (if in a later step a ModuleNotFoundError occurs, download the package listed with the error)
	 - download Nodejs from the Nodejs website. It is highly recommended that you get the LTS version as they are stable: https://nodejs.org/en/
2. Download the repo to a dedicated directory, ideally called **Reach-Sentinel-Lite**
	 - `git init`
	 - `git clone https://github.com/Bruin-Spacecraft-Group/Reach-Sentinel-Lite`

3. You should now see the files in your directory

4. Navigate into the repo you just cloned, then go into **reachSentinelLite**
	 - Check to see if it contains the **bin** folder
	 - If it does, run `source bin/activate` -> this activates the virtual environment

5. To start the server, run: `python3 manage.py runserver`
	 - DO NOT USE `python` to use python2 - the code is written in python3

6. Open a browser and navigate to: http://127.0.0.1:8000/dashboard/

7. If your website isn't working, it may mean that the database has not been initialized.
	 - `python3 manage.py makemigrations`
	 - `python3 manage.py migrate`

8. Final step is to open up a new terminal window and run `python3 manage.py shell`, then `exec(open("main.py").read())`
	 - This establishes a connection to the ground station
	 - Saves incoming data to database

## TODO
