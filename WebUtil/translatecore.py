# Adding necessary imports
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as edgeservice
from selenium.webdriver.edge.service import Service as chromeservice
from selenium.webdriver.chrome.options import Options as chromeoptions
from selenium.webdriver.edge.options import Options as edgeoptions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

class TranslateCore:
    # Class params
    def __init__(self, chrome_driver="./chromedriver_win32\chromedriver.exe", edge_driver="./edgedriver_win64\msedgedriver.exe", \
                    microsoft_translation_url = "https://www.bing.com/translator?ref=MsftMT", \
                        google_translation_url="https://translate.google.com/", \
                            use_edge = True, use_headless=False) -> None:
        
        self.use_edge = use_edge

        if use_edge:
            options = edgeoptions()
            options.headless = use_headless
            self.edge_service = edgeservice(executable_path=edge_driver)
            self.driver = webdriver.Edge(service=self.edge_service, options=options)

        else:
            options = chromeoptions()
            options.headless = use_headless
            self.chrome_service = chromeservice(executable_path=chrome_driver)
            self.driver = webdriver.Chrome(service=self.chrome_service, options=options)
        
        self.microsoft_translation_url = microsoft_translation_url
        self.google_translation_url = google_translation_url

        # Testing edge and chrome browser
        # self.driver.get(self.microsoft_translation_url)
        
    def translate_text_to_lang(self, text="كيفكم", translation_lang_key="EN", \
        use_single_service = False, use_microsoft=False)->List:        
        """
        Takes text as input and gives output using Microsoft and Google Translate
        @params:
        text : input text
        translation_lang : output translation lang (currently just supports to en)

        """
        
        output_translations = []
        if not use_single_service:
            microsoft_translation = self.translate_using_microsoft_translate(text=text, translation_lang_key=translation_lang_key)
            print(microsoft_translation)
            #Testing language translation other than english
            self.translate_using_google_translate(text=text, translation_lang_key=translation_lang_key)

    def translate_using_microsoft_translate(self, text:str, translation_lang_key="EN")->str:
        # Opening the URL
        self.driver.get(self.microsoft_translation_url)
        
        # Selecting output language
        language_selection = None
        try:
            language_selection = os.getenv(translation_lang_key)
        
        except:
            # Setting fallback in case of dict lookup failure
            language_selection = "English"
        
        # print(language_selection)
        # Setting translation language from dropdown
        output_language_dropdown = Select(self.driver.find_element(by="xpath", value=r'//select[@id="tta_tgtsl"]'))
        output_language_dropdown.select_by_visible_text(language_selection)

        # Sending input text for translation
        input_text_box = self.driver.find_element(by="xpath", value=r'//textarea[@id="tta_input_ta"]')
        # print(type(input_text_box))
        input_text_box.send_keys(text)
        
        #Extracting translated text
        output_text_box = self.driver.find_element(by="xpath", value=r'//textarea[@id="tta_output_ta"]')
        while output_text_box.get_attribute('value') == '' or output_text_box.get_attribute('value') == ' ...':
            continue
        
        translated_text = output_text_box.get_attribute('value')
        return translated_text
    
    # TODO Have to add language selection feature in Google Translate
    def translate_using_google_translate(self, text:str, translation_lang_key="EN"):
        self.driver.get(self.google_translation_url)
        # Selecting output language
        language_selection = None
        try:
            language_selection = os.getenv(translation_lang_key)
        
        except:
            # Setting fallback in case of dict lookup failure
            language_selection = "English"
        
        if translation_lang_key == "EN":
            #TODO Directly enter the text and get the output
            select_input_text_box = self.driver.find_element(by="xpath", value=r'//textarea[@aria-label="Source text"]')
            select_input_text_box.send_keys(text)
            #While text shows as translating
            wait = WebDriverWait(self.driver, 2)
            select_output_text_box = wait.until(ec.visibility_of_element_located((By.XPATH, r'//span[@class="Q4iAWc"]')))
            select_output_text_box = self.driver.find_element(by="xpath", value=r'//span[@class="Q4iAWc"]')
            print(select_output_text_box.text)
            
        else:
            select_language_from_dropdown = self.driver.find_element(by="xpath", value=r'//button[@jsname="zumM6d"]')
            select_language_from_dropdown.send_keys(Keys.ENTER)
            time.sleep(0.50)
            select_output_language_input_box = self.driver.find_elements(by="xpath", value=r'//input[@class="yFQBKb" and @jsaction="input:G0jgYd;" and @jsname="oA4zhb"]')[1]
            select_output_language_input_box.send_keys(language_selection)
            language_sanity_check = self.driver.find_element(by="xpath", value=r'//div[@class="dykxn C96yib j33Gae"]/div[@class="vSUSRc" and @jsname="mm30Mc"]/div')
            
            # Adding logic for language sanity check and checking if Google supports the translation
            val = language_sanity_check.text 
            if val == 'No results':
                # If language to translate not supported fallback to English
                select_output_language_input_box.clear()
                select_output_language_input_box.send_keys("English")
                
            select_output_language_input_box.send_keys(Keys.ENTER)
            # select_output_language_input_box.send_keys(Keys.ENTER)  

            select_input_text_box = self.driver.find_element(by="xpath", value=r'//textarea[@aria-label="Source text"]')
            select_input_text_box.send_keys(text)

            #While text shows as translating
            wait = WebDriverWait(self.driver, 2)
            select_output_text_box = wait.until(ec.visibility_of_element_located((By.XPATH, r'//span[@class="Q4iAWc"]')))
            # print(select_output_text_box)
            select_output_text_box = self.driver.find_element(by="xpath", value=r'//span[@class="Q4iAWc"]')
            # print(select_output_text_box)
            print(select_output_text_box.text)

    def process_excel(filepath="./Text.xlsx"):
        pass
