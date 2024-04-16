import os
import time
from selenium import webdriver
from dotenv import load_dotenv, find_dotenv
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager
from selenium.webdriver.chrome.service import Service as ChromeService

dotenv_path = find_dotenv()  # finds the .env file path
load_dotenv(dotenv_path)  # loads the .env file from the path found above

PROMISED_UP = 10
PROMISED_DOWN = 800
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
USERNAME = os.getenv('TWITTER_USERNAME')

SPEED_TEST_URL = 'https://www.speedtest.net/'
TWITTER_URL = 'https://twitter.com/home'


class InternetSpeedTwitterBot:
    def __init__(self):
        self.up = 0
        self.down = 0
        chrome_driver_path = ChromeDriverManager().install()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option(name="detach", value=True)
        # Keep the browser open when the script finishes - unless you use driver.quit()

        service = ChromeService(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        self.get_internet_speed()
        print(self.down)
        if float(self.down) < PROMISED_DOWN:
            self.tweet_at_provider()

        time.sleep(10)
        self.driver.quit()

    def get_internet_speed(self):
        self.driver.get(SPEED_TEST_URL)  # Goes to the speedtest website
        time.sleep(1)  # Gives the page time to load
        start_button = self.driver.find_element(by=By.CLASS_NAME, value='start-button')
        start_button.click()  # Starts the speed test
        time.sleep(30)
        self.down = self.driver.find_element(by=By.CLASS_NAME, value='download-speed').text
        self.up = self.driver.find_element(by=By.CLASS_NAME, value='upload-speed').text

    def tweet_at_provider(self):
        self.driver.get(TWITTER_URL)
        time.sleep(3)

        # Enter email then proceed to the next screen
        email_field = self.driver.find_element(by=By.NAME, value='text')
        email_field.send_keys(USERNAME)
        time.sleep(1.25)  # Gives the page time to
        next_button = self.driver.find_element(
            by=By.XPATH,
            value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]'
        )
        next_button.click()
        time.sleep(1)

        # Enter the password then login
        password_field = self.driver.find_element(by=By.NAME, value='password')
        password_field.send_keys(PASSWORD)
        login_button = self.driver.find_element(
            by=By.XPATH,
            value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div'
        )
        login_button.click()
        time.sleep(2.15)

        # Screen will now show the homepage of Twitter
        # Compose tweet and post it
        tweet_input = self.driver.find_element(
            by=By.CSS_SELECTOR,
            value='div[class="public-DraftStyleDefault-block public-DraftStyleDefault-ltr"]')
        tweet_input.click()
        time.sleep(.5)
        tweet_input.send_keys(f"@Comcast my internet speeds have dropped to {self.down}mbps down when I "
                              f"am paying for {PROMISED_DOWN} down")

        post_button = self.driver.find_element(by=By.XPATH,
                                               value='//*[@id="react-root"]/div/div/div['
                                                     '2]/main/div/div/div/div/div/div[3]/div/div[2]/div['
                                                     '1]/div/div/div/div[2]/div[2]/div[2]/div/div/div['
                                                     '2]/div[3]')
        post_button.click()
