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
import customize
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
from selenium.common.exceptions import NoSuchElementException

import pyfiglet
from pyfiglet import figlet_format

log = logging.getLogger(__name__)

# Initialize the start-up functions
def start_up():
    setup_logger()
    key = wrapper(gui)
    relay_choice(key)

# Function to call logger,
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

# Function for calling gui elements
def gui(stdscr):
    stdscr.clear()
    stdscr.refresh()
    f = figlet_format('ART DASH', font = "colossal", justify = 'left')
    for i, char in enumerate(f): 
        time.sleep(0.002)
        stdscr.addch(char)
        stdscr.refresh()
    stdscr.refresh()
    stdscr.addstr(9,0,
        "------------------------------------------------------------------------------"
        )
    stdscr.refresh()
    stdscr.addstr(10,0,"Version 1.0")
    stdscr.refresh()
    stdscr.addstr(11,0,"")
    
    def print_dots():
        dots = "...."
        for dot in dots:
            curses.delay_output(500)
            stdscr.addstr(dot)
            stdscr.refresh()
    
    print_dots()
   
    stdscr.addstr(12,0,"Please select One of the following Options:", curses.A_REVERSE)
    stdscr.addstr(13,0,"Twitter > Reddit [1]")
    stdscr.addstr(14,0,"Twitter [2]")
    stdscr.addstr(15,0,"")

    while True:
        key = stdscr.getkey()
        if key == "1":
            stdscr.addstr(16,0,"Art Post Selected")
            print_dots()
            break
        else:
            stdscr.addstr(16,0,"None")
            break

    if key == range(1,2):
        stdscr.addstr(17,0,"Press any key to continue")

    stdscr.refresh()
    time.sleep(2)
    stdscr.getch()
    return key

# Function to collect the choices and pass on the confirmation to modules
def relay_choice(key):
    if key == '1':
        TwitterBot()
        ImgurBot()
        RedditBot()
    if key == '2':
        TwitterBot()

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

# Moves cursor and presses buttons to emulate human input (after every major button press)
def avoid_lock():
    x, _ = pyautogui.position()
    pyautogui.moveTo(x + 200, pyautogui.position().y, duration=1.0)
    pyautogui.moveTo(x, pyautogui.position().y, duration=0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('esc')
    pyautogui.keyUp('ctrl')
    time.sleep(0.5)
    pyautogui.press('esc')

# Class for Twitter program
class TwitterClass:

    # Initialize init object
    def __init__(self,
                 username,
                 password,
                 post,
                 upload=[]):
        
        log.info("Starting Twitter Bot")
        dirpath = os.getcwd()
        log.info("Current directory is : " + dirpath)
        
        self.options = browser_options()
        self.browser = launch_driver()
        self.wait = WebDriverWait(self.browser, 30)
        self.start_twitter(username, password)
        # self.post_twitter(upload, post)
        twitter_link = self.twitter_link()
        self.write_to_file(upload, post, twitter_link)

    # Log in to Twitter
    def start_twitter(self, username, password):
        log.info("Logging in.....Please wait")
        self.browser.get("https://twitter.com/i/flow/login")
        log.info("Waiting for elements to load... ")
        time.sleep(random.uniform(3,5))
        try:
            user_field = self.browser.find_element(By.XPATH,
                "//input[@autocomplete='username']"
                )
            next_button = self.browser.find_element(By.XPATH,
                "//div[@role='button']/div/span/span[contains(., 'Next')]"
                )
            user_field.send_keys(username)
            time.sleep(random.uniform(1.5,2.5))
            next_button.click()
            time.sleep(random.uniform(1.5,2.5))
            login_button = self.browser.find_element(By.XPATH,
                "//div[@data-testid='LoginForm_Login_Button']"
                )
            pw_field = self.browser.find_element(By.XPATH,
                "//input[@name='password']"
                )
            pw_field.send_keys(password)
            time.sleep(random.uniform(1.5,2.5))
            login_button.click()
            time.sleep(random.uniform(1.5,2.5))
            log.info("Login successful")
        except TimeoutException:
            log.info(
                "TimeoutException! Username/password field or login button not found"
                )

    # Send the (image and) text and post tweet
    def post_twitter(self, upload, post):
        # Lock out test
        avoid_lock()
        log.info("Lock avoided.")

        log.info("Writing Tweet... ")
        try:
            start_tweet_bttn = self.browser.find_element(By.XPATH,
                "//a[@href='/compose/tweet']"
                )
            start_tweet_bttn.click()
            time.sleep(random.uniform(1.5,2.5))
            text_input = self.browser.find_element(By.XPATH,
                "//div[@data-testid='tweetTextarea_0']"
                )
            text_input.click()
            #text_input.send_keys(post)
            time.sleep(random.uniform(1.5,2.5))
            upload_tweet_bttn = self.browser.find_element(By.XPATH,
                    "//div[@data-testid='tweetButton']"
                    )
            img_input = self.browser.find_element(By.XPATH,
                "//input[@accept='image/jpeg,image/png,image/webp,image/gif,video/mp4,video/quicktime']"
                )

            if len(upload) > 0:
                for img in upload:
                    img_input.send_keys(img)
                txt_upload = text_input.send_keys(post)
                log.info(f"{len(upload)} image(s) and text submitted")
            else:
                txt_upload = text_input.send_keys(post)
                log.info("Text-only post submitted")

            time.sleep(5)
            # upload_tweet_bttn.click()
        except TimeoutException:
            log.info(
                "TimeoutException! Upload data or Twitter buttons not found"
                )


    # Get the link to the tweet just sent
    def twitter_link(self):
        # Lock out test
        avoid_lock()
        log.info("Lock avoided.")

        time.sleep(5)
        log.info("Getting link... ")
        profile_button = self.browser.find_element(By.XPATH,
            "//a[@aria-label='Profile']"
            )
        profile_button.click()
        time.sleep(random.uniform(1.5,2.5))

        tweets = self.browser.find_elements(By.XPATH,
            "//article[@data-testid='tweet']"
            )

        # wait for scroll to happen
        time.sleep(5)
        ## change later to scroll by element from ref code for OScar
        self.browser.execute_script("arguments[0].scrollIntoView(true);", tweets[2])
        time.sleep(5)
        log.debug(f"Tweets found: {tweets}")
        share_button = tweets[1].find_element(By.XPATH, 
            "//div[@aria-label='Share Tweet']"
            )
        self.browser.execute_script("arguments[0].click();", share_button)
        
        time.sleep(random.uniform(1.5,2.5))
        
        # Press the button to copy link to clipboard
        share_link = tweets[1].find_element(By.XPATH,
            "//div[@role='menuitem']/div[2]/div/span[contains(., 'Copy link to Tweet')]"
            )
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable(share_link)).click()
        link = pyperclip.paste()
        log.debug(link)
        
        # upload clipboard to yaml immediately
        data = str(pyperclip.paste())
        dataY = dict(twit_link = data)

        with open('twit.yaml', 'w') as outfile:
            yaml.dump(dataY, outfile, default_flow_style=False)
    
    # Upload logs to .csv for reference
    def write_to_file(self, upload, post, twitter_link):
    
        filename = "output.csv"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        toWrite = [timestamp, upload, post, twitter_link]
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(toWrite)
            log.info(f"Activity recorded in {filename}")
        log.info("Twitter module completed")

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
        time.sleep(random.uniform(1.5,2.5))
        # Navigate Imgur DOM
        try:
            upload_button = self.browser.find_element(By.XPATH,
                "//input[@id='file-input']"
                )
            time.sleep(random.uniform(1.5,2.5))
            upload_button.send_keys(upload)
            time.sleep(12) ##until loaded
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
            log.debug(f"Clipboard: {str(pyperclip.paste())}")

            # Copy link to yaml 
            log.info("Saving link...")
            data = str(pyperclip.paste()) 
            # Fixing the link string
            job = data.replace('[/img]','').replace('[img]', '')  
            dataY = dict(img_link = job)
            
            with open('imgur.yaml', 'w') as outfile:
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
        self.red_write_to_file(img_link, choice, red_title)

    # Log in to Reddit
    def start_reddit(self, red_username, red_password): 
        try:
            log.info("Logging in.....Please wait")
            self.browser.get("https://www.reddit.com/login/")
            avoid_lock()
            log.info("Waiting for elements to load... ")
            time.sleep(random.uniform(1.5,2.5))
            
            # Reddit's JavaScript is buggy, clicking this link and then going back fixes issue
            glitch_fix = tweets = self.browser.find_element(By.XPATH,
                "//a[@class='BottomLink']"
                )
            glitch_fix.click()
            self.browser.back()
            time.sleep(random.uniform(1.5,2.5))

            username_box = self.browser.find_element(By.XPATH,
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
            time.sleep(random.uniform(1.5,2.5))
            password_box.click()
            password_box.send_keys(red_password)
            time.sleep(random.uniform(1.5,2.5))
            login_buttn.click()

            # If the site JavaScript is still stuck, reload the loop (and page)
            elem = WebDriverWait(self.browser, 100).until(
                      EC.presence_of_element_located((By.XPATH, "//input[@type='search']"))
                      )

            while True:    
                if not elem:
                    log.debug("Reddit log-in reload executed")
                    continue
                else:
                    break
            
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
        self.browser.refresh()

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
                time.sleep(random.uniform(1.5,2.5))
                
                red_search.send_keys(Keys.ENTER)
                time.sleep(random.uniform(1.5,2.5)) 

                #Toggle safe search button for proper results
                try:
                    safe_search = self.browser.find_element(By.XPATH,
                            "//button[@id='safe-search-toggle']"
                            )
                    safe_search.click()
                except NoSuchElementException:
                    log.error("Safe search button could not be verified. Closing system")
                    break

                ##CHANGE to unitl.loaded later on (the list doesn't update very fast)
                time.sleep(random.uniform(3,5))
                # Subreddit name (sub_list)
                sub_name = self.browser.find_element(By.XPATH, 
                        "//h6[contains(., '" +subs+ "')]" 
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
                
                flair_picked = False
                for element in flair_menu:
                    try:
                        log.debug("//div[@role='radiogroup']/div[" +flair_key+"]")
                        flair = self.browser.find_element(By.XPATH,"//div[@role='radiogroup']/div[" +flair_key+"]") 
                        clicked = flair.click()
                        flair_picked = True
                        if clicked:
                            log.info(f"Inserted flair: {flair}")
                    except NoSuchElementException:
                        log.error("Flair tag cannot be found") 
                        time.sleep(3)
                        webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()

                if flair_picked == True:
                    apply_bttn = self.browser.find_element(By.XPATH,
                        "//button[contains(., 'Apply')]"
                        )
                    apply_bttn.click()

                submit_bttn = self.browser.find_element(By.XPATH,
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

    # Import twitter keys
    assert parameters['username'] is not None
    assert parameters['password'] is not None

    username = parameters.get('username')
    password = parameters.get('password')
    upload = parameters.get('upload', [])
    post = parameters.get('post')

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

    def TwitterBot():
        TwitterClass(username=username,
                     password=password,
                     upload=upload,
                     post=post)

    def ImgurBot():
        ImgurClass(upload=upload)

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

    start_up()
