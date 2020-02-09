"""
I wish I had a better solution. :(
Let me know if you discover one,
or if Twitter adds poll support to its API.
"""

import json
from time import sleep
from selenium import webdriver
import selenium.common.exceptions

Keys = webdriver.common.keys.Keys

def tweet_poll(question):
    driver = webdriver.Firefox()

    #these cookies store our login session.
    #it might expire eventually.
    with open("cookies.json","r") as file:
        cookies = json.load(file)

    #navigate to domain so we can set the cookies
    driver.get("https://twitter.com")

    for cookie in cookies:
        if "expiry" in cookie:
            #not entirely sure why i have to do this
            cookie["expiry"] = int(cookie["expiry"])
        driver.add_cookie(cookie)

    driver.get("https://twitter.com/compose/tweet")
    
    actions = webdriver.ActionChains(driver)
    #let all the javascript settle down
    actions.pause(16)
    #type the tweet. the box should already be focused.
    actions.send_keys(question)
    #navigate to the add poll button
    actions.send_keys(Keys.TAB * 3)
    #press the add poll button
    actions.send_keys(Keys.ENTER)
    #wait for poll card to slide in
    actions.pause(1)
    actions.perform()

    #now that these exist, find them
    choice1_box = driver.find_element_by_name("Choice1")
    choice2_box = driver.find_element_by_name("Choice2")

    actions = webdriver.ActionChains(driver)
    #type into the answer boxes
    actions.send_keys_to_element(choice1_box, "yes")
    actions.send_keys_to_element(choice2_box, "no")
    #navigate to the Tweet button
    actions.send_keys(Keys.TAB * 8)
    #press the tweet button
    actions.send_keys(Keys.ENTER)
    #wait for the tweet to send before we quit
    actions.pause(4)
    actions.perform()
    
    driver.quit()

if __name__ == "__main__":
    tweet_poll("This is a test tweet.")
