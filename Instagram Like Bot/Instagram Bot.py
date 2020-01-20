from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from math import ceil
import os
from getpass import getpass


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
        time.sleep(1)
        driver.get("https://www.instagram.com/" + name + "/")
        time.sleep(2.5)

        pic_hrefs = []
        temp = []
        while True:
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

                temp.append(len(pic_hrefs))
                length = len(temp)

                if(length == 5):
                    if(len(set(temp)) <= 1):
                        break
                    else:
                        temp.clear()

                if(len(pic_hrefs) >= no_of_pics_to_like):
                    break

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

        try:
            pic_hrefs = pic_hrefs[:no_of_pics_to_like]
        except Exception:
            pass

        # liking photos
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            svg_aria_label = driver.find_element_by_tag_name(
                "svg").get_attribute("aria-label")
            like_button_xpath = '//button[@class="wpO6b "]'
            time.sleep(0.5)

            msg = ''
            post_liked = False

            while not post_liked:
                try:
                    if(svg_aria_label == "Like"):
                        driver.find_element_by_xpath(like_button_xpath).click()

                        no_of_likes += 1

                        msg = f"{no_of_likes}. Liked {pic_href}"
                        post_liked = True
                        time.sleep(0.5)
                    else:
                        no_of_likes += 1
                        post_liked = True
                        msg = f"{no_of_likes}. Already liked {pic_href}"
                        time.sleep(0.5)
                except Exception as e:
                    time.sleep(2)
                    continue

                if(post_liked):
                    print(msg)
                    f.write(msg + "\n")
                    break

        print(f"\n\nTOTAL NUMBER OF POSTS LIKED : {no_of_likes}\n")
        f.write(f"\n\nTOTAL NUMBER OF POSTS LIKED : {no_of_likes}\n")

        f.close()


name = input("Enter Instagram Name to like photos on : ")
no_of_pics_to_like = int(
    input("Enter Number Of Posts to Like : "))
file_name = name

email = input("Enter Your Instagram ID : ")
password = getpass(prompt="Enter Your Instagram Password : ")

BOT = InstagramBot(email, password)
BOT.login()
BOT.like_photo(name, no_of_pics_to_like)
BOT.closeBrowser()
