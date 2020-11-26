# Reach-Sentinel-Lite


## Quick start for native Linux / Mac

1. First, you must download the following:
	 - download Django from the Django website, ideally for python-3: https://www.djangoproject.com/
	 - download Docker from the Docker website: https://hub.docker.com/?overlay=onboarding

2. Download the repo to a dedicated directory, ideally called **Reach-Sentinel-Lite**
	 - `git init`
	 - `git clone https://github.com/Bruin-Spacecraft-Group/Reach-Sentinel-Lite`

3. You should now see the files in your directory

4. Navigate into the repo you just cloned
	 - You should see the **Dockerfile** and **Makefile** files
	 - Make sure you have Docker successfully installed and running

5. To build and start the server, run: `make`

6. Open a browser and navigate to: http://0.0.0.0:8000/dashboard/
	 - The above link may not always work, so try this: http://0.0.0.0:8000/temp/

## Quick start for Ubuntu Subsystem in Windows

1. If you haven't already pulled Reach-Sentinel-Lite, run 
	- $ git clone https://github.com/Bruin-Spacecraft-Group/Reach-Sentinel-Lite.git

2. Then, in order to go into the directory, run 
	- $ cd Reach-Sentinel-Lite

3. Then, in order to switch the branch to docker-try, which is the most recently-updated one, run
 	- $ git checkout docker-try 

4. Git will do its thing, and at this point you should have all of the files you need to run the server.
But if you run the server now, your browser might not be able to connect to 0.0.0.0:8000, and as a result you won't see the website. So first, run
 	- $ ifconfig 

5. Copy the IP address next to the  "inet" label under eth0 by highlighting it and then right clicking. 
Linux uses right click instead of Ctrl-C for copying because Linux is cursed.
Now, run
 	- $ nano reachSentinelLite/reachSentinelLite/settings.py 

6. Find the ALLOWED_HOSTS array and paste the address you copied into it by pressing the right mouse button. 
Make sure that it's surrounded in quotations and properly separated with commas from the other elements.
Close nano by pressing Ctrl-X and then pressing Enter to save over the old settings file.
Now you're ready to run
 	- $ make 

7. Let Docker do its stuff and eventually you'll see a message like "PRESS CTRL-C TO EXIT" or something. This means that the server is running. 2 or 3 errors might pop up, but you can ignore those.
	- Open Chrome or Firefox or whatever and go to (that address you copied):8000/dashboard.
	- For me, the URL would look like 172.22.195.128:8000/dashboard.
	- You should now see the webpage.

## TODO
