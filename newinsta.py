from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from random import randint
from time import sleep
import logging
import sqlite3
import tensorlayer as tl
from train import inference, model_

class NewInsta:
    def __init__(self, username, password, headless=True, instapy_workspace=None):
	    
        self.selectors = {
            "home_to_login_button": ".WquS1 a",
            "username_field": "username",
            "password_field": "password",
            "button_login": "._0mzm-",
            "search_user": "queryBox",
            "select_user": "._0mzm-",
            "textarea": "textarea",
            "send": "button"
        }

        # Creating driver 
        if headless == True:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        else:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

        # Going to google
        # self.driver.get("https://instagram.com")
        # sleep(1)

        # # Starting search by inputing query
        # self.driver.find_element_by_xpath("//input[@name=\"q\"]").send_keys(query)
        # self.driver.find_element_by_xpath("//input[@name=\"q\"]").send_keys(Keys.RETURN)
        # self.driver.submit()


    def login(self, username, password):
        # homepage
        self.driver.get('https://instagram.com')
        self.__randomSleep__(3, 5)
        self.driver.find_element_by_name(
            self.selectors['username_field']).send_keys(username)
        self.driver.find_element_by_name(
            self.selectors['password_field']).send_keys(password)
        self.driver.find_element_by_css_selector("button[type='submit']").click()
        # self.driver.submit()
        # self.driver.get('https://www.instagram.com/direct/inbox/')

        logging.info('Logged In')
        
        self.__randomSleep__()

    def __randomSleep__(self, min = 2, max = 10):
        t = randint(min, max)
        logging.info('Wait {} seconds'.format(t))
        sleep(t)

    def followingPeople(self):
        pass

    def getMessages(self):
        pass

    def sendMessage(self, user, message):
        
        logging.info('Send message {} to {}'.format(message, user))
        self.driver.get('https://www.instagram.com/direct/new/')
        
        self.__randomSleep__(1,2)
        
        # Try to dismiss notification
        try:
            # Looping through buttons of page
            buttons = self.driver.find_elements_by_tag_name('button')
            for button in buttons:
                print(button.text)
                if button.text == 'Not Now':
                    print('aaa')
                    button.click()
                    break
        except Exception as e:
            logging.error(e)

        # Importing user in query
        self.driver.find_element_by_name(
            self.selectors['search_user']).send_keys(user)
        self.__randomSleep__()

        # Select user
        divs = self.driver.find_elements_by_tag_name('div')
        for div in divs:
            if div.text == user:
                accountButton = div
                print('found div')
                break

        accountButton.click()
        self.__randomSleep__(1, 2)

        # Clicking next
        for div in divs:
            if div.text == 'Next':
                div.click()
                break
        
        # Go to page
        self.__randomSleep__()
        self.driver.find_elements_by_xpath("*//textarea")[0].send_keys(message)

        self.__randomSleep__()
        buttons = self.driver.find_elements_by_css_selector(self.selectors['send'])
        buttons[len(buttons)-1].click()

        self.__randomSleep__()

    def sendGroupMessage(self, users, message):
        logging.info('Send message {} to {}'.format(message, users))
        self.driver.get('https://www.instagram.com/direct/new/')

        self.__randomSleep__(1, 2)

        # Try to dismiss notification
        try:
            # Looping through buttons of page
            buttons = self.driver.find_elements_by_tag_name('button')
            for button in buttons:
                print(button.text)
                if button.text == 'Not Now':
                    print('aaa')
                    button.click()
                    break
        except Exception as e:
            logging.error(e)

        # Select user
        for user in users:

            # Importing user in query
            self.driver.find_element_by_name(
                self.selectors['search_user']).send_keys(user)
            self.__randomSleep__()
            
            divs = self.driver.find_elements_by_tag_name('div')
            for div in divs:
                if div.text == user:
                    accountButton = div
                    print('found div')
                    break
            print('eferger')
            print(accountButton)
            self.driver.execute_script("arguments[0].click();", accountButton)
            self.__randomSleep__(1, 2)

        # Clicking next
        for div in divs:
            if div.text == 'Next':
                div.click()
                break

        # Go to page
        self.__randomSleep__()
        self.driver.find_elements_by_xpath("*//textarea")[0].send_keys(message)

        self.__randomSleep__()
        buttons = self.driver.find_elements_by_css_selector(
            self.selectors['send'])
        buttons[len(buttons)-1].click()

        self.__randomSleep__()

    def listener(self):
        # Trying to load model to get response
        try:
            load_weights = tl.files.load_npz(name='model.npz')
            tl.files.assign_weights(load_weights, model_)
        except Exception as e:
            print(e)
            print('AI not connected')
            return False

        self.driver.get('https://www.instagram.com/direct/inbox/')
        self.__randomSleep__()
        
        # Try to dismiss notification
        try:
            # Looping through buttons of page
            buttons = self.driver.find_elements_by_tag_name('button')
            for button in buttons:
                print(button.text)
                if button.text == 'Not Now':
                    print('aaa')
                    button.click()
                    break
        except Exception as e:
            logging.error(e)
        
        self.__randomSleep__()
        originalSourceCode = self.driver.page_source
        counter = 0
        self.openMessage()
        while True:
            counter += 1
            print('iteration', counter)
            self.__randomSleep__(3, 5)
            newSourceCode = self.driver.page_source
            if originalSourceCode == newSourceCode:
                print('same')
            else:
                print('changed')
                self.openMessage()
                originalSourceCode = self.driver.page_source
    def openMessage(self):
        
        unansweredConvos = []
        # Getting unanswered convos
        aTags = self.driver.find_elements_by_tag_name('a')
        for link in aTags:
            href = link.get_attribute("href") 
            if '/direct/t/' in href:
                print('convo div')
                print(href)

                # Checking length of divs
                aTagDiv = link.find_element_by_tag_name('div')
                divChildren = aTagDiv.find_elements_by_xpath('./*')

                # print(divChildren)
                # divChildrenList = []
                # for div in divChildren:
                #     divChildrenList.append(div)
                print(len(divChildren))
                if len(divChildren) == 3:
                    print('unanswered convo')
                    unansweredConvos.append(aTagDiv)

        # # Getting time tags
        # timeTags = self.driver.find_elements_by_tag_name('time')

        # currentTimeNow = []
        # for time in timeTags:
        #     if time.text == 'Now':
        #         currentTimeNow.append(time)
        
        # print(currentTimeNow)

        # Looping through unanswered messages
        for conversation in unansweredConvos:
            
            # Going into conversation
            conversation.click()

            self.__randomSleep__(3, 5)

            # Getting most recent message
            message = self.driver.find_elements_by_tag_name('span')[-1]
            print("message.text")
            print(message.text)
            
            self.__randomSleep__(1, 3)
            
            responses = []
            top_n = 1
            for i in range(top_n):
                sentence = inference(message.text, top_n)
                sentence = ' '.join(sentence)
                print(sentence)
                responses.append(sentence)

            self.driver.find_elements_by_xpath("*//textarea")[0].send_keys(sentence)
            self.__randomSleep__()
            buttons = self.driver.find_elements_by_css_selector(
                self.selectors['send'])
            buttons[len(buttons)-1].click()
            self.driver.get('https://www.instagram.com/direct/inbox/')


        
