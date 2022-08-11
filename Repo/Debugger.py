
import curses
import csv
import time
import random
import os
import logging
import tweepy
import pyautogui
import yaml
import pyperclip
#import pyYAML
from curses import wrapper
from selenium import webdriver
from datetime import datetime, timedelta
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException ##IMPROT

## Debug driver config
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
chrome_driver = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver,options=chrome_options)

log = logging.getLogger(__name__)

#from selenium.common.exceptions import NoSuchElementException
import customize

def setup_logger():  # set up creation of log archive and log.info
    dt = datetime.strftime(datetime.now(), "%m_%d_%y %H_%M_%S ")

    if not os.path.isdir('./logs'):
        os.mkdir('./logs')

    logging.basicConfig(filename=('./logs/' + str(dt) + 'artDash.log'),
                        filemode='w',
                        format='%(asctime)s::%(name)s::%(levelname)s::%(message)s',
                        datefmt='./logs/%d-%b-%y %H:%M:%S')

    log.setLevel(logging.DEBUG)
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)
    c_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
    c_handler.setFormatter(c_format)
    log.addHandler(c_handler)

# Set options for the web browser driver
def browser_options():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")

    # Disable webdriver flags or you will be easily detectable
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return options

# Launches the Selenium Chrome driver
# def launch_driver():
#     driver = webdriver.Chrome(ChromeDriverManager().install())
#     return driver

def avoid_lock():
    x, _ = pyautogui.position()
    pyautogui.moveTo(x + 200, pyautogui.position().y, duration=1.0)
    pyautogui.moveTo(x, pyautogui.position().y, duration=0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('esc')
    pyautogui.keyUp('ctrl')
    time.sleep(0.5)
    pyautogui.press('esc')


class RedditClass:

    def __init__(self, 
                 red_username, 
                 red_password, 
                 post, 
                 twit_link, 
                 img_link,
                 sub_list,
                 red_title,
                 nsfw,
                 choice=[]):

        log.debug(f"Choice = {choice}")
        log.info("Starting Reddit Bot")
        dirpath = os.getcwd()
        log.info("Current directory is : " + dirpath)

        self.options = browser_options()
        self.browser = driver
        self.wait = WebDriverWait(self.browser, 30)
        # self.start_reddit(red_username, red_password)
        self.post_reddit(post, twit_link, img_link, sub_list, red_title, nsfw, choice)
        # self.red_write_to_file(img_link, choice, red_title)

#START DEBUG EDITS
####--------------------------####

    # Send post and format tags and text
    def post_reddit(self, 
                    post, 
                    twit_link, 
                    img_link, 
                    sub_list,
                    red_title,
                    nsfw,
                    choice):

        # Get selected subs    
        def get_key(choice, sub_list):
            temp = []
            for i in choice:
                for key, value in sub_list.items():
                    if i == value:
                        temp.append(key)
            return temp
                    
        sub_choice = get_key(choice, sub_list)

        log.debug(nsfw)

        if nsfw == 'y':
            nsfw_tag = self.browser.find_element(By.XPATH,
                    "//button[@aria-label='Mark as Not Safe For Work']"
                    )
            nsfw_tag.click()
            log.info("NSFW tag clicked")
        else:
            log.info("NSFW tag skipped")
            pass

    # END DEBUG EDITS
    ###------------------------------###


if __name__ == '__main__':

    with open("config.yaml", 'r') as stream:
        try:
            parameters = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc
        
    # Import Reddit keys
    assert parameters['red_username'] is not None
    assert parameters['red_password'] is not None

    red_username = parameters.get('red_username')
    red_password = parameters.get('red_password')
    post = parameters.get('post')
    twit_link = parameters.get('twit_link')
    img_link = parameters.get('img_link')
    sub_list = parameters.get('sub_list')
    red_title = parameters.get('red_title')
    nsfw = parameters.get('NSFW')
    choice = parameters.get('choice', [])

    # Import Twitter link clipboard
    with open("twit.yaml", 'r') as stream:
        try:
            twitfile = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc

    twit_link = twitfile.get('twit_link')

    # Import Imgur link clipboard
    with open("imgur.yaml", 'r') as stream:
        try:
            imgrfile = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc

    img_link = imgrfile.get('img_link')

    def RedditBot():
        RedditClass(red_username=red_username, 
                    red_password=red_password,
                    post=post,
                    twit_link=twit_link, 
                    img_link=img_link,
                    sub_list=sub_list,
                    red_title=red_title,
                    nsfw=nsfw,
                    choice=choice)
        


    log.debug(f"Choice = {choice}")
    setup_logger()

    RedditBot()
#--remote-debugging-port=9222
