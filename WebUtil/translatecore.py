# Adding necessary imports
from typing import Dict, List
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
from tqdm import tqdm

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
        use_single_service = False, use_microsoft=False)->Dict:        
        """
        Takes text as input and gives output using Microsoft and Google Translate
        @params:
        text : input text
        translation_lang : output translation lang (currently just supports to en)

        """
        #TODO Optimize page refresh and create UI
        
        output_translations = {}
        if not use_single_service:
            self.driver.get(self.microsoft_translation_url)
            output_translations["microsoft"] = self.translate_using_microsoft_translate(text=text, translation_lang_key=translation_lang_key)
            print(output_translations["microsoft"])
            #Testing language translation other than english
            self.driver.get(self.google_translation_url)
            output_translations["google"] = self.translate_using_google_translate(text=text, translation_lang_key=translation_lang_key)
            
        else: 
            if use_microsoft:
                self.driver.get(self.microsoft_translation_url)
                output_translations["microsoft"] = self.translate_using_microsoft_translate(text=text, translation_lang_key=translation_lang_key)
            
            else:
                self.driver.get(self.google_translation_url)
                output_translations["google"] = self.translate_using_google_translate(text=text, translation_lang_key=translation_lang_key)
        print(output_translations)
        return output_translations

    def translate_using_microsoft_translate(self, text:str, translation_lang_key="EN")->str:
        # Opening the URL

        
        # Selecting output language
        language_selection = os.getenv(translation_lang_key, default="English")
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
        input_text_box.clear()
        return translated_text
    
    def translate_using_google_translate(self, text:str, translation_lang_key="EN", \
                                            return_dummy=True):
        if return_dummy == True:
            return "[INFO] Returning Dummy dor Google Translate"

        # Selecting output language
        language_selection = os.getenv(translation_lang_key, default="English")
        output_translation = ""

        if translation_lang_key == "EN":
            select_input_text_box = self.driver.find_element(by="xpath", value=r'//textarea[@aria-label="Source text"]')
            select_input_text_box.send_keys(text)
            #While text shows as translating
            wait = WebDriverWait(self.driver, 6)
            select_output_text_box = wait.until(ec.visibility_of_element_located((By.XPATH, r'//span[@class="ryNqvb"]')))
            select_output_text_box = self.driver.find_element(by="xpath", value=r'//span[@class="ryNqvb"]')
            output_translation = select_output_text_box.text
            # print(select_output_text_box.text)
            select_input_text_box.clear()
            
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
            wait = WebDriverWait(self.driver, 5)
            select_output_text_box = wait.until(ec.visibility_of_element_located((By.XPATH, r'//span[@class="ryNqvb"]')))
            # print(select_output_text_box)
            select_output_text_box = self.driver.find_element(by="xpath", value=r'//span[@class="ryNqvb"]')
            # print(select_output_text_box)
            output_translation = select_output_text_box.text
            # print(select_o  utput_text_box.text)
            select_input_text_box.clear()
        return output_translation

    #Optimized functions for batch processing a list of utterances
    def optimized_process(self, utterance_list:List=[], \
                            translation_lang_key="EN", \
                                use_both_services=True,
                                return_dummy_for_google=True):

        if use_both_services:
            output_json = {}
            google_translate_li = []
            microsoft_translate_li = []
            print("[INFO] Processing Microsoft Engine")
            for idx, text in tqdm(enumerate(utterance_list), total=len(utterance_list) ):
                if text == "Empty Utterance":
                    continue
                self.driver.get(self.microsoft_translation_url)
                microsoft_translate_li.append(self.translate_using_microsoft_translate(text=text, translation_lang_key=translation_lang_key))
            print("[INFO] Processing Google Engine")
            for idx, text in tqdm(enumerate(utterance_list), total=len(utterance_list) ):
                if text == "Empty Utterance":
                    continue
                self.driver.get(self.google_translation_url)
                google_translate_li.append(self.translate_using_google_translate(text=text, translation_lang_key=translation_lang_key, \
                                        return_dummy=return_dummy_for_google))
            output_json["google"] = google_translate_li
            output_json["microsoft"] = microsoft_translate_li
            print(output_json)
            return output_json

    def process_excel(self, filepath="./Text.xlsx", \
                        outputpath="./OutputText.xlsx",\
                            translation_lang_key="EN", return_dummy_for_google=True):
        # excel_entity = {
        #     "Bot Input": [],
        #     "Microsoft Translate": [],
        #     "Google Transalte": []
        # }

        # df = pd.DataFrame.from_dict(excel_entity)
        df_to_process = None
        if os.path.exists(filepath):
            if filepath.split(".")[-1] == "csv":
                df_to_process = pd.read_csv(filepath)
            elif filepath.split(".")[-1] == "xlsx":
                df_to_process = pd.read_excel(filepath)
            else:
                return "[INFO] File format not supported currently"
        else:
            return "[INFO] No Input file found"
        df_to_process_copy = df_to_process.fillna("Empty Utterance")
        to_translate_list = df_to_process_copy["UTTERANCES"].to_list()
        # for val in to_translate_list:
        #     if val == "Empty Utterance":
        #         continue
        #     output_json = self.translate_text_to_lang(text=val, use_single_service=False, \
        #                                     translation_lang_key=translation_lang_key)
        #     series_obj = pd.Series([val, output_json['microsoft'], output_json['google']], index=df.columns)
        #     df = df.append(series_obj, ignore_index=True)
            
        output_json = self.optimized_process(to_translate_list,\
                                                translation_lang_key=translation_lang_key, \
                                                    return_dummy_for_google=return_dummy_for_google)
        df = pd.DataFrame.from_dict(output_json)
        result = pd.concat([df_to_process, df], axis=1)
        result.to_excel(outputpath, index=False)
        self.driver.close()
        return "[INFO] Processed all the Excel files"
        