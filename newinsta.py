from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from random import randint, choice
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

        # Defining list of greetings
        self.greetings = [
            'hello',
            'hey',
            'Yo',
            'Wsp',
            'Wyd'
            'Hi'
        ]

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
        self.username = username


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
        
        self.driver.execute_script("arguments[0].click();", accountButton)
        self.__randomSleep__(1, 2)

        # Clicking next
        for div in divs:
            try:
                if div.text == 'Next':
                    self.driver.execute_script("arguments[0].click();", div)
                    break
            except Exception as e:
                print(e)
                continue
        
        # Go to page
        self.__randomSleep__()
        self.driver.find_elements_by_xpath("*//textarea")[0].send_keys(message)


        self.__randomSleep__()
        print('clicking button')
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
                    self.driver.execute_script("arguments[0].click();", button)
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
                self.driver.execute_script("arguments[0].click();", div)
                break

        # Sending message
        self.__randomSleep__()
        self.driver.find_elements_by_xpath("*//textarea")[0].send_keys(message)

        self.__randomSleep__()
        buttons = self.driver.find_elements_by_css_selector(
            self.selectors['send'])
        buttons[len(buttons)-1].click()

        self.__randomSleep__()

    def automatic(self, hitUpChance=100, checkUp=1000):

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

        self.__randomSleep__(1, 3)
        
        # Trying to open requests
        self.acceptRequest()
            
        # Creating infinate loop
        while True:
            
            counter += 1
            print('iteration', counter)
            
            self.__randomSleep__(3, 5)
            newSourceCode = self.driver.page_source
            
            # Checking if page changed
            if originalSourceCode == newSourceCode:
                print('same')
            else:
                print('changed')
                self.openMessage()
                originalSourceCode = self.driver.page_source

            # Checking for random chance when bot will follow a user and message or message an already existing friend
            # if randint(0, hitUpChance) < 1:
            self.hitUp()

            # elif randint(0, checkUp) < 1:
            #     self.checkUp()
    
    def acceptRequest(self):
        print('looking at request')

        while True:
            self.driver.get('https://www.instagram.com/direct/requests/')
            self.__randomSleep__(3, 5)
            # Looping through request and accepting
            # Getting unanswered convos
            requests = self.driver.find_elements_by_tag_name('a')
            requestUrlList = []
            for request in requests:
                href = request.get_attribute("href") 
                if '/direct/t/' in href:
                    print('request div')
                    print(href)
                    requestUrlList.append(request)
            
            if len(requestUrlList) == 0:
                self.driver.get('https://www.instagram.com/direct/inbox/')
                break

            for request in requestUrlList:
                request.click()
                self.__randomSleep__(3, 5)
                divs = self.driver.find_elements_by_tag_name('div')
                for div in divs:
                    print(div.text)
                    if div.text == 'Accept':
                        div.click()
                        print('Clicked Accept')
                        break
                break

            print(requestUrlList)
            print("requestUrlList")
                        
        
    
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
            
            self.replyToMessage(message.text)
            self.driver.get('https://www.instagram.com/direct/inbox/')

    def hitUp(self):
        print('following and hitting someone up')

        # Going to followers page
        username = self.username
        profilePage = f"https://instagram.com/{username}/"
        self.driver.get(profilePage)

        # Clicking the following button
        links = self.driver.find_elements_by_tag_name('a')
        for link in links:
            href = link.get_attribute("href") 
            print(href)
            if '/following/' in href:
                self.driver.execute_script("arguments[0].click();", link)
                break
        
        self.__randomSleep__(1, 3)

        divTags = self.driver.find_elements_by_tag_name('div')
        for div in divTags:
            roleDiv = div.get_attribute("role")
            if roleDiv == 'dialog':
                print('found role with dialog')
                break
        
        followingLinks = []
        # Getting list of users
        buttonTags = div.find_elements_by_tag_name('button')
        for button in buttonTags:
            buttonType = button.get_attribute("type")
            if button.text == 'Following':
                parentDiv = button.find_element_by_xpath('../..')
                
                # Getting a tag
                aTag = parentDiv.find_elements_by_tag_name('a')
                print(len(aTag))
                print("len(aTag)")
                for tag in aTag:
                    aTagTitle = tag.get_attribute("title")
                    if tag.text:
                        if aTagTitle == tag.text:
                            print('found')
                            followingLinks.append(tag)
                        print(tag.text)
        
        friendElement = choice(followingLinks)
        self.__randomSleep__(1, 3)

        self.driver.execute_script("arguments[0].click();", friendElement)
        
        self.__randomSleep__(1, 3)

        # Clicking followers
        aTags = self.driver.find_elements_by_tag_name('a')
        for tag in aTags:
            link = tag.get_attribute("href") 
            if '/followers/' in link:
                self.driver.execute_script("arguments[0].click();", tag)
                print('wow')
                break

        self.__randomSleep__(1, 3)
        
        # Getting list of users
        unorderedLists = self.driver.find_elements_by_tag_name('ul')
        
        # Getting main list of followers
        for ul in unorderedLists:
            print('ayee')
            try:
                listDiv = ul.find_element_by_tag_name('div')
                liTag = listDiv.find_elements_by_tag_name('li')
            except Exception as e:
                continue
        
        print('clicking')
        friendElement = choice(liTag)
        self.__randomSleep__(1, 3)
        
        link = friendElement.find_element_by_tag_name('a')
        self.driver.execute_script("arguments[0].click();", link)

        self.__randomSleep__(1, 3)
        # Following and messaging person
        header = self.driver.find_element_by_tag_name('section')
        
        print('Following')
        # Getting button with follow in it
        buttons =  header.find_elements_by_tag_name('button')
        for button in buttons:
            if button.text == 'Follow':
                button.click()

        self.__randomSleep__(1, 3)
        print('Clicking message')
        # Getting spans with message in it
        buttons =  header.find_elements_by_tag_name('button')
        for button in buttons:
            if button.text == 'Message':
                self.driver.execute_script("arguments[0].click();", button)
                print('clicked message')
                break

        self.__randomSleep__(1, 3)
        # Sending greating message
        self.replyToMessage()

        self.driver.get('https://www.instagram.com/direct/inbox/')

    def checkUp(self):
        self.driver.get("https://www.instagram.com/direct/inbox/")
        print('dismissing notification')
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
        
        print('Checking up on someone')

        self.__randomSleep__()
        unansweredConvos = []
        
        # Getting unanswered convos
        aTags = self.driver.find_elements_by_tag_name('a')
        print(len(aTags))
        for link in aTags:
            href = link.get_attribute("href") 
            if '/direct/t/' in href:
                unansweredConvos.append(link)

        print(unansweredConvos)
        friendDiv = choice(unansweredConvos)
        self.driver.execute_script("arguments[0].scrollIntoView();", friendDiv)
        friendDiv.click()
        self.__randomSleep__()

        # Sending greating message
        self.replyToMessage()


    # GENERAL PURPOSE FUNCTIONS
    def replyToMessage(self, message=None):
        
        print('dismissing notification')
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
        
        if message:
            top_n = 1
            for i in range(top_n):
                sentence = inference(message, top_n)
                sentence = ' '.join(sentence)
                print(sentence)
                responses.append(sentence)
        else:
            sentence = choice(self.greetings)
        
        self.__randomSleep__()
        self.driver.find_elements_by_xpath("*//textarea")[0].send_keys(sentence)

        self.__randomSleep__()
        buttons = self.driver.find_elements_by_css_selector(
            self.selectors['send'])
        buttons[len(buttons)-1].click()

        self.__randomSleep__()
