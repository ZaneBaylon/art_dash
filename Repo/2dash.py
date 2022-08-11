## imgur -> reddit modules

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

log = logging.getLogger(__name__)
###----------------------------###

#from selenium.common.exceptions import NoSuchElementException
import customize

pghold = time.sleep(random.uniform(1.5,2.5)) ##IMPORT into merged version

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
def launch_driver():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver

def avoid_lock():
    x, _ = pyautogui.position()
    pyautogui.moveTo(x + 200, pyautogui.position().y, duration=1.0)
    pyautogui.moveTo(x, pyautogui.position().y, duration=0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('esc')
    pyautogui.keyUp('ctrl')
    time.sleep(0.5)
    pyautogui.press('esc')

####--------------------------####


class ImgurClass:

    def __init__(self, upload):
        
        log.info("Starting Imgur Bot")
        dirpath = os.getcwd()
        log.info("Current directory is : " + dirpath)

        self.options = browser_options()
        self.browser = launch_driver()
        self.wait = WebDriverWait(self.browser, 30)
        self.upload = upload
        self.start_imgur(upload)
    
    def start_imgur(self, upload):
        
        log.info("Logging in.....Please wait")
        self.browser.get("https://imgur.com/upload")
        log.info("Waiting for elements to load... ")
        pghold
        # Navigate Imgur DOM
        try:
            upload_button = self.browser.find_element(By.XPATH,
                "//input[@id='file-input']"
                )
            pghold
            upload_button.send_keys(upload)
            time.sleep(12) ##until loaded
            ## might need to finaggle the visibility if so: executor.execute_script("arguments[0].click();", ele)
            drop_down = self.browser.find_element(By.XPATH,
                "//div[@class='Dropdown image-options']"
                )
            self.browser.execute_script("arguments[0].click();", drop_down)
            
            options_button = self.browser.find_element(By.XPATH,
                "//button[@class='Dropdown-option'][contains(., 'Get share links')]"
                )
            self.browser.execute_script("arguments[0].click();", options_button)
            
            link_button = self.browser.find_element(By.XPATH,
                "//div[contains(., 'BBCode (Forums)')]/following::button[contains(., 'Copy Link')]"
                )
            link_button.click()

            ##idunno in case the other one doesn't work
            #"//div[contains(., 'BBCode (Forums)')]/parent::div[@class='ShareOptionsDialog-link']/div[2]/div/button[@class='CopyUrl-button ShareOptionsDialog-link--button']"

            log.debug(f"Clipboard: {str(pyperclip.paste())}")

            time.sleep(1000) # db

            # Copy link to yaml 
            log.info("Saving link...")

            data = str(pyperclip.paste())
            
            # Fixing the link string
            job = data.replace('[/img]','').replace('[img]', '')
            
            dataY = dict(img_link = job)
            
            with open('imgur.yaml', 'a') as outfile:
                yaml.dump(dataY, outfile, default_flow_style=False)

            log.info("Imgur module completed")

        except TimeoutException:
            log.info(
                "TimeoutException! Username/password field or login button not found"
                )


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
        self.browser = launch_driver()
        self.wait = WebDriverWait(self.browser, 30)
        self.start_reddit(red_username, red_password)
        self.post_reddit(post, twit_link, img_link, sub_list, red_title, nsfw, choice)
        #self.get_key(choice, sub_list) ##already called by post_reddit
        self.red_write_to_file(img_link, choice, red_title)

    # Log in to Reddit
    def start_reddit(self, red_username, red_password): 
        try:
            log.info("Logging in.....Please wait")
            self.browser.get("https://www.reddit.com/login/")
            log.info("Waiting for elements to load... ")
            pghold 
        
            pghold
            username_box = tweets = self.browser.find_element(By.XPATH,
                "//input[@id='loginUsername']"
                )
            password_box = self.browser.find_element(By.XPATH,
                "//input[@id='loginPassword']"
                )
            login_buttn = self.browser.find_element(By.XPATH,
                "//button[@class='AnimatedForm__submitButton m-full-width']"
                )
            username_box.click()
            username_box.send_keys(red_username)
            pghold

            password_box.click()
            password_box.send_keys(red_password)
            pghold

            login_buttn.click()
            
        except TimeoutException:
            log.info(
                "TimeoutException! Username/password field or login button not found"
                )

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

        # Give Reddit time to load 
        try:
            elem = WebDriverWait(self.browser, 50).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='search']"))
            )
        except TimeoutException:
            log.error("No elements loaded")

        # lock out test
        avoid_lock()
        log.info("Lock avoided.")

        # Start loop
        for subs in sub_choice:
            try:
                # Find searchbar, hit delete  
                red_search = self.browser.find_element(By.XPATH,
                        "//input[@type='search']"
                        )
                self.browser.execute_script("arguments[0].click();", red_search)

                red_search.send_keys(subs)
                red_search.click()

                ##REPLACE time.sleep with wait until loaded later
                ##MAKE SURE safe search is turned off; add in later

                time.sleep(random.uniform(1.5,2.5))
                
                red_search.send_keys(Keys.ENTER)
                time.sleep(random.uniform(1.5,2.5)) 

                # Subreddit name (sub_list)
                sub_name = self.browser.find_element(By.XPATH, 
                        "//h6[contains(., " +subs+ ")]" 
                        )
                sub_name.click()
                time.sleep(random.uniform(1.5,2.5))

                ##execute click (sometimes there is an overlay that might mess things up)
                sub_post = self.browser.find_element(By.XPATH,
                        "//input[@name='createPost']"
                        )
                sub_post.click()
                time.sleep(random.uniform(1.5,2.5))

                link_post = self.browser.find_element(By.XPATH,
                        "//button/i[@class='_3WIAbYQQdSmuuFLDSfhn5_ icon icon-link_post']"
                        )
                link_post.click()
                time.sleep(random.uniform(1.5,2.5))

                post_title = self.browser.find_element(By.XPATH,
                        "//textarea[@placeholder='Title']"
                        )

                # Title of img (red_title)
                post_title.send_keys(red_title)
                time.sleep(random.uniform(1.5,2.5))

                # Body of post
                post_body = self.browser.find_element(By.XPATH,
                        "//textarea[@placeholder='Url']"
                        )
                post_body.send_keys(img_link)
                time.sleep(random.uniform(1.5,2.5))
                
                # oc_tag = self.browser.find_elements(By.XPATH,
                #         "//button[@role='button']/i/span[contains(., OC)]"
                #         )

                # NSFW tag 
                if nsfw == 'y':
                    nsfw_tag = self.browser.find_element(By.XPATH,
                            "//button[@aria-label='Mark as Not Safe For Work']"
                            )
                    nsfw_tag.click()
                    log.info("NSFW tag clicked")
                else:
                    log.info("NSFW tag skipped")
                    pass

                flair_tag = self.browser.find_element(By.XPATH,
                        "//button[@aria-label='Add flair']"
                        )
                flair_tag.click()
                time.sleep(random.uniform(1.5,2.5))

                # Import customize function
                flair_key = customize.parse_flair(red_title)

                flair_menu = self.browser.find_elements(By.XPATH,
                        "//div[@aria-label='flair_picker']/div[@aria-checked='false']"
                        )
                
                for element in flair_menu:
                    try:
                        flair = element.find_element(By.XPATH,"//div[@role='radiogroup']/div[" +flair_key+"]") 
                        clicked = flair.click()
                        if clicked:
                            log.info(f"Inserted flair: {flair}")
                    except NoSuchElementException:
                        log.error("Flair tag cannot be found")
                        pass
                        
                apply_bttn = self.browser.find_element(By.XPATH,
                        "//button[contains(., 'Apply')]"
                        )
                apply_bttn.click()

                submit_bttn = self.browser.find_elements(By.XPATH,
                        "//button[@role='button'][contains(., 'Post')]"
                        )
                submit_bttn.click()
                log.info("Reddit post submitted")

                time.sleep(random.uniform(1.5,2.5))

                comment_box = self.browser.find_element(By.XPATH,
                        "//div[@class='notranslate public-DraftEditor-content']"
                        )
                comment_box.click()
                comment_box.send_keys("Original post may be found here: " +twit_link+ "")

                comment_buttn = self.browser.find_element(By.XPATH,
                        "//button[@role='button'][contains(., 'Comment')]"
                        )
                comment_buttn.click()
                log.info("Reddit comment added")

            except TimeoutException:
                log.error("Failed to write post")
                break

    def red_write_to_file(self, img_link, choice, red_title):
    
        filename = "output.csv"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        toWrite = [timestamp, img_link, choice, red_title]
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(toWrite)
            log.info(f"Activity recorded in {filename}")
        log.info("Reddit module completed")



# Import yaml data
if __name__ == '__main__':

    with open("config.yaml", 'r') as stream:
        try:
            parameters = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc


    ###------------------------------###

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
    nsfw = parameters.get('nsfw')
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

    setup_logger()
    log.debug(f"Choice = {choice}")
    ##REMEMBER to add in the imgur format after merging branches
    ##CONSIDER making all time.sleep commands into one variable after merge
    RedditBot()
