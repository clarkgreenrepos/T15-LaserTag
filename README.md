<h1 align="center">Team 15 Laser Tag Software<br />
<div align="center">
<a href="https://github.com/clarkgreenrepos/T15-LaserTag">
<img src="https://raw.githubusercontent.com/clarkgreenrepos/T15-LaserTag/refs/heads/main/img/photon_logo.png" title="Logo" style="max-width:100%" width="512" /></a>
</div></h1>
Laser Tag Software for CSCE 35103 - Software Engineering Section 001

## Installing Libraries<br/>
Intalling Pip<br/>
- Pip is a package manager for Python that allows easy installs of libraries that may be required during development.To install, follow these steps:<br/>
	- In linux, open the terminal and enter `sudo apt update`, then `sudo apt install python3-pip`.
	- Enter password if prompted
	- To check that pip is properly installed, enter `pip3 --version`. If pip is installed, the version number and other information will be displayed.

Installing libraries<br/>
- Using pip, we will now install the required libraries. Most of the libraries used in this program come standard with Python but some need to be installed separately. The libraries we are going to install are "Tkinter", "psycopg2", and "Pillow".
	- For Tkinter, we actually won't use pip but, instead, enter `sudo apt-get install python3-tk` into the terminal. Tkinter may already be installed as it is a common graphics library so, this is more of a "just in case" step.
	- For psycopg2, enter `pip3 install psycopg2`.
	- For Pillow, enter `pip3 install Pillow`.

## How To Run<br/>
Run `python3 main.py` In terminal<br/>
- A window will open and after `3` seconds the splash screen will appear, then disappear after another `3` Seconds, finally after `1` second the player screen is displayed.<br/>

- In one of the `ID No.` inputs, input a six digit ID number and then press enter.<br/>
- A window will be displayed prompting you for a new code name<br/> 
	- The code Name Cannot Contain the following characters 
	- `!@#$%^&*()_+\-=\[\]{};\':\"\\|,.<>/?~` 
- after typing in a valid code name and clicking submit a new prompt will appear asking for your `Equipment ID`
	- the Equipment ID must be a two digit Number
- After clicking submit You regain access to the player screen.
- Add all the players you wish
- settings
	- if you want to remove all players click the Reset teams button
	- if you want to change the ip click the `network address` button
- to start click `start Game`
	- Not implemented
 
<br/><br/>

## Language<br/>
Python<br/><br/>



## GITHUB MEMBERS<br/>
clarkgreenrepos - **Matthew Clark Green** <br/>
BraedenBarlow - **Braeden Barlow**<br/>
ColinPhifer - **Colin Phifer**<br/>
TimothyShaneEwing - **Tim Ewing**<br/>