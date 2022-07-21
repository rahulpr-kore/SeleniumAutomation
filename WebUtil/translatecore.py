# Adding necessary imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as edgeservice
from selenium.webdriver.edge.service import Service as chromeservice
# import pandas as pd

class TranslateCore:
    # Class params
    def __init__(self, chrome_driver="", edge_driver="", \
                    microsoft_translation_url = "https://www.bing.com/translator?ref=MsftMT", \
                        google_translation_url="https://translate.google.com/") -> None:
        
        # self.chrome_service = chromeservice(executable_path="./chromedriver_win32/chromedriver.exe")
        self.edge_service = edgeservice(executable_path="./edgedriver_win64\msedgedriver.exe")
        # self.chrome_driver = webdriver.Edge(service=chrome_driver)
        self.edge_driver = webdriver.Edge(service=self.edge_service)
        self.microsoft_translation_url = microsoft_translation_url
        self.edge_driver.get(self.microsoft_translation_url)