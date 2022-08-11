import curses
import time, random, os
import logging
import tweepy
from curses import wrapper
from selenium import webdriver
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
import yaml 


log = logging.getLogger(__name__)
# Idk if I actually need this. If I'm api surfing then no, don't initialize this
#driver = webdriver.Chrome(ChromeDriverManager().install())

# Function to call logger, gui elements
def startUp():
	
	setupLogger()
	key = wrapper(gui)
	relayChoice(stdscr)

def setupLogger():  # set up creation of log archive and log.info
    dt = datetime.strftime(datetime.now(), "%m_%d_%y %H_%M_%S ")

    #if not os.path.isdir('./logs'):
        #os.mkdir('./logs')
 
    logging.basicConfig(filename=('./logs/' + str(dt) + 'artDash.log'), filemode='w',
                        format='%(asctime)s::%(name)s::%(levelname)s::%(message)s', datefmt='./logs/%d-%b-%y %H:%M:%S')
    log.setLevel(logging.DEBUG)
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)
    c_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
    c_handler.setFormatter(c_format)
    log.addHandler(c_handler)

# Function for calling gui elements
def gui(stdscr):
	stdscr.clear()
	stdscr.refresh()
	stdscr.addstr(0,0,"Welcome to ArtDash")
	#time.sleep(0.5)
	stdscr.refresh()
	stdscr.addstr(1,0,"Version 1.0")
	#time.sleep(0.9)
	stdscr.refresh()
	stdscr.addstr(2,0,"")
	
	def print_dots():
		dots = "...."
		for dot in dots:
			curses.delay_output(500)
			stdscr.addstr(dot)
			stdscr.refresh()
	
	print_dots()
	
	#time.sleep(0.5)
	stdscr.addstr(3,0,"Please select One of the following Options:", curses.A_REVERSE)
	stdscr.addstr(4,0,"Art Post [1]")
	stdscr.addstr(5,0,"")	

	while True:
		key = stdscr.getkey()
		if key == "1":
			stdscr.addstr(5,0,"Art Post Selected")
			print_dots()
			break
		else:
			stdscr.addstr(5,0,"None")
			break

	if key == "1":
		stdscr.addstr(6,0,"Press any key to continue")

	stdscr.refresh()
	time.sleep(2)
	stdscr.getch()
	return key

# function to collect the choices and pass on the confirmation to modules
def relayChoice(stdscr):
	if key == '1':
		twitterBot()
		# from here you're gunna have to somehow launch both the twitter class and a gui screen (maybe)

# Class for main program
class twitter :

	# Initialize init object
	def __init__(self,
				 twit_api_key,
				 twit_api_secret,
				 twit_access_token,
				 twit_access_secret,
				 uploads,
				 status):
		
		self.tweepy = tweepy
		self.uploads = uploads
		self.status = status
		authorize = self.twitterAuth(twit_api_key, twit_api_secret)
		sendToken = self.twitterToken(twit_access_token, twit_access_secret)
		api = self.tweepy.API(self.auth)
		sendUploads = self.twitterUpload(uploads, status, api)

	# Authorize api
	def twitterAuth(self, twit_api_key, twit_api_secret):
		
		if len(twit_api_key) > 0 and len(twit_api_secret) > 0: 
			self.auth = self.tweepy.OAuthHandler(twit_api_key, twit_api_secret)
			log.info("Twitter keys found")
		else:
			error.log("Could not find Twitter keys")

	# Send token
	def twitterToken(self, twit_access_token, twit_access_secret):
		
		if len(twit_access_token) > 0 and len(twit_access_secret) > 0:
			token = self.auth.set_access_token(twit_access_token, twit_access_secret)
			api = self.tweepy.API(self.auth)
			log.info("Twitter token found")
		else:
			error.log("Could not find Twitter tokens")

        	# Send post		
	def twitterUpload(self, uploads, status, api):
		
		if len(uploads) > 0:	
			update_media = api.update_with_media(self.uploads, self.status)
			log.info(f"{len(uploads)} image(s) posted")
		else: 
			update_text = api.update_status(self.status)
			log.info("Text-only status posted")
			pass

# Import yaml data
if __name__ == '__main__':

    with open("config.yaml", 'r') as stream:
        try:
            parameters = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc

	# Import twitter keys
    twit_api_key = parameters.get('twit_api_key')
    twit_api_secret = parameters.get('twit_api_secret')
    twit_access_token = parameters.get('twit_access_token')
    twit_access_secret = parameters.get('twit_access_secret')
    uploads = '' # probably like the yaml to an image folder, take the next in line
    status = "test" # possibly have this be a string from the image description in the metadata? idk how that works. I don't want to have to dig in the yaml 

    twitterBot = twitter(twit_api_key=twit_api_key,
                         twit_api_secret=twit_api_secret,
                         twit_access_token=twit_access_token,
                         twit_access_secret=twit_access_secret,
                         uploads=uploads,
                         status=status
                       )
    startUp()
