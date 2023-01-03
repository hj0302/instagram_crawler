
import os
import pandas as pd
import time
from glob import glob
import json
import random
import requests
import traceback

import logger

import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

class InstaCrawler():

    def __init__(self, insta_id, insta_pw, n):
        self.FILE_PATH = os.getcwd()
        self.DIR_PATH  = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        self.CHROME_DRIVER_PATH = f'{self.FILE_PATH}/chromedriver'
        self.SAVE_XLSX_PATH = f'{self.DIR_PATH}/rsc/follower_list/'
        self.IMPLICITYLY_WAIT_NUM = 180
        self.CRAWL_FOLLOW_NUM = n
        self.MAIN_URL = f'https://www.instagram.com/'
        self.INSTA_ID = insta_id
        self.INSTA_PW = insta_pw
        self.logger = logger.get_logger()

    def execute_sleep(self, start_num, end_num):
        '''
        스크래핑 차단당하는 것을 방지하기 위해 time sleep 실행해주는 함수
        '''
        random_num = random.uniform(start_num, end_num)
        return time.sleep(random_num)

    def execute_chromedriver(self):
        '''
        Selenium Chrome Driver Open
        '''
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(executable_path=self.CHROME_DRIVER_PATH, options=chrome_options)
            driver.implicitly_wait(self.IMPLICITYLY_WAIT_NUM)
            
            self.execute_sleep(30, 180)

            return driver
        except Exception as ex:
            self.logger.warning('Chrome Driver Execute Error')
            raise Exception('Chrome Driver Execute Error')

    def login_insta(self, driver):
                        
        '''
        Instagram Login
        '''
        try :
            driver.get(url=self.MAIN_URL)
        except:
            self.logger.warning('Instagram Main Url Access Not')
            raise Exception('Instagram Main Url Access Not')

        self.execute_sleep(30, 180)

        id_box = driver.find_element(By.CSS_SELECTOR, '#loginForm > div > div:nth-child(1) > div > label > input')
        password_box = driver.find_element(By.CSS_SELECTOR, '#loginForm > div > div:nth-child(2) > div > label > input')
        login_button = driver.find_element(By.CSS_SELECTOR, '#loginForm > div > div:nth-child(3) > button')

        try :
            act = ActionChains(driver) #동작 명령어 지정
            act.send_keys_to_element(id_box, self.INSTA_ID).send_keys_to_element(password_box, self.INSTA_PW).click(login_button).perform() #아이디 입력, 비밀 번호 입력, 로그인 버튼 클릭 수행 
        except Exception as ex:
            self.logger.warning(f'Instagram Login Not -  Insta ID : {self.INSTA_ID}')
            raise Exception('Instagram Login Not')

        self.execute_sleep(30, 180)

        request_session = requests.Session()

        headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}
        request_session.headers.update(headers)

        for cookie in driver.get_cookies():
            c = {cookie['name'] : cookie['value']}
            request_session.cookies.update(c)

        return request_session

    def crawl_follwer_list(self, request_session, userid):
        insta_user_url = f'https://www.instagram.com/api/v1/friendships/{userid}/followers/?count={self.CRAWL_FOLLOW_NUM}&search_surface=follow_list_page'
        try :
            response = request_session.get(insta_user_url)
        except Exception as ex:
            self.logger.warning(f'Instagram Crawl Not -  Insta ID : {self.INSTA_ID}, Crwal ID : {uesrid}')
            raise Exception(f'Instagram Crawl Not')

        if response.status_code == 200:
            content = response.text
            content_dict = json.loads(content)
            content_df = pd.DataFrame(content_dict['users'])
            content_df.to_excel(f'{self.SAVE_XLSX_PATH}/{userid}.xlsx', index=False)
            self.logger.info(f'Instagram Crawl Success -  Insta ID : {self.INSTA_ID}, Crwal ID : {userid}')
        else :
            self.logger.warning(f'Instagram Crawl Response Not 200 -  Insta ID : {self.INSTA_ID}, Crwal ID : {userid}')
        
        #time.sleep(1800 + execute_sleep(600, 1800))

class InstaUserKnow():

    def __init__(self):
        self.FILE_PATH = os.path.dirname(__file__)
        self.DIR_PATH  = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        self.INSTA_USERID_PATH = f'{self.DIR_PATH}/rsc/knowledge/crawl_user_list.xlsx'

    def get_insta_user_list(self):
        '''
        수집해야될 인스타그램 유저 목록을 가져오는 함수
        '''

        def get_completed_insta_user_list(self):
            '''
            이미 수집이 완료된 인스타그램 유저 목록을 가져오는 함수
            '''

            completed_userid_list = glob(f'{self.DIR_PATH}/rsc/follower_list/*.xlsx')
            completed_userid_list = [ int(i.split('/')[-1].replace('.xlsx', '')) for i in completed_userid_list]
            return completed_userid_list

        completed_userid_list = get_completed_insta_user_list(self)

        df = pd.read_excel(self.INSTA_USERID_PATH)
        df = df[~df['id'].isin(completed_userid_list)]
        userid_list = df['id'].unique().tolist()
        
        return userid_list


if __name__ == "__main__":
    insta_id = ''
    insta_pw = ''

    _userknow = InstaUserKnow()
    _crawler = InstaCrawler(insta_id, insta_pw, n)
    
    crawl_user_list = _userknow.get_insta_user_list()

    driver = _crawler.execute_chromedriver()
    request_session = _crawler.login_insta(driver)
    for userid in crawl_user_list[:1]:
        _crawler.crawl_follwer_list(request_session, userid)
