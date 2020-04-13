import os
from time import sleep

from selenium import webdriver
from dotenv import load_dotenv


load_dotenv()


class InstaBot:
    def __init__(self, username, password):
        self.url = 'https://instagram.com'
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.get(self.url)
        self.unfollowers = []
        self.followers = []
        sleep(2)
        self.username = username
        self.password = password
        self.login()
        sleep(5)

    def login(self):
        username_input = self.driver.find_element_by_xpath('//input[@name=\"username\"]').send_keys(self.username)
        password_input = self.driver.find_element_by_xpath('//input[@name=\"password\"]').send_keys(self.password)
        login_button = self.driver.find_element_by_xpath('//button[@type=\"submit\"]')
        login_button.click()

    def ignore_popup(self):
        self.driver.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()

    def get_unfollowers(self):
        self.driver.find_element_by_xpath(f'//a[contains(@href, "/{self.username}")]').click()

        suggestions_text = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
        self.driver.execute_script('arguments[0].scrollIntoView()', suggestions_text)
        sleep(1)

        scroll_box = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        last_height, height = 0, 1
        while last_height != height:
            last_height = height
            height = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        print(names)


my_bot = InstaBot(
    username=os.getenv('INSTAGRAM_USERNAME'),
    password=os.getenv('INSTAGRAM_PASSWORD')
)
my_bot.ignore_popup()
my_bot.get_unfollowers()

"""
# run with `python -i main.py`
# next go to your profile with my_bot.get_unfollowers
"""
