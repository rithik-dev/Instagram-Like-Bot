from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from math import ceil
import os


def clearFile():
    f = open(f"C:\\Users\\{os.getlogin()}\\Desktop\\{file_name}.txt", "w")
    f.write("")
    f.close()


dir_path = os.path.dirname(__file__) + "\\chromedriver.exe"


class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(dir_path)

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)
        user_name_elem = driver.find_element_by_xpath(
            "//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath(
            "//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(2)

    def like_photo(self, name, no_of_pics_to_like):
        driver = self.driver
        driver.get("https://www.instagram.com/" + name + "/")
        time.sleep(1.5)

        scroll_times = 10
        if no_of_pics_to_like <= 24:
            scroll_times = 2
        else:
            scroll_times = int(ceil(no_of_pics_to_like / 12))

        pic_hrefs = []
        for i in range(1, scroll_times):
            try:
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.5)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href)
                 for href in hrefs_in_view if href not in pic_hrefs]

            except Exception:
                continue

        no_of_likes = 0

        clearFile()

        f = open(
            f"C:\\Users\\{os.getlogin()}\\Desktop\\{file_name}.txt", "a")

        print(
            f"\n\nStarted Liking {no_of_pics_to_like} Posts on \'{name}\' :-\n")
        f.write(
            f"Started Liking {no_of_pics_to_like} Posts on \'{name}\' :-\n\n")

        # liking photos

        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(1.5)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            try:
                driver.find_element_by_xpath(
                    '//button[@class="wpO6b "]').click()
                no_of_likes += 1
                print(f"{no_of_likes}. {pic_href}")
                f.write(f"{no_of_likes}. {pic_href}\n")
                if no_of_likes == no_of_pics_to_like:
                    print(f"\n\nTOTAL NUMBER OF POSTS LIKED : {no_of_likes}\n")
                    f.write(
                        f"\n\nTOTAL NUMBER OF POSTS LIKED : {no_of_likes}\n")
                    break
                time.sleep(0.5)
            except Exception as e:
                while True:
                    try:
                        driver.find_element_by_xpath(
                            '//button[@class="wpO6b "]').click()
                        no_of_likes += 1
                        print(f"{no_of_likes}. {pic_href}")
                        f.write(f"{no_of_likes}. {pic_href}\n")
                        time.sleep(0.5)
                        break
                    except:
                        time.sleep(2)

        f.close()


name = input("Enter Instagram Name to like photos on : ")
no_of_pics_to_like = int(
    input("Enter Number Of Recent Posts to Like : "))
file_name = name

email = input("Enter Your Instagram ID : ")
password = input("Enter Your Instagram Password : ")

i_love_coding_ = InstagramBot(email, password)
i_love_coding_.login()
i_love_coding_.like_photo(name, no_of_pics_to_like)
i_love_coding_.closeBrowser()
