# Adding necessary imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as edgeservice
from selenium.webdriver.edge.service import Service as chromeservice
import pandas as pd

class TranslateCore:
    # Class params
    def __init__(self, chrome_driver="./chromedriver_win32\chromedriver.exe", edge_driver="./edgedriver_win64\msedgedriver.exe", \
                    microsoft_translation_url = "https://www.bing.com/translator?ref=MsftMT", \
                        google_translation_url="https://translate.google.com/", \
                            browser_choice = "Edge") -> None:
        
        if browser_choice == "Edge":
            self.edge_service = edgeservice(executable_path=edge_driver)
            self.edge_driver = webdriver.Edge(service=self.edge_service)

        else:
            self.chrome_service = chromeservice(executable_path=chrome_driver)
            self.chrome_driver = webdriver.Chrome(service=self.chrome_service)
        
        self.microsoft_translation_url = microsoft_translation_url
        self.google_translation_url = google_translation_url

        # Testing edge and chrome browser
        self.edge_driver.get(self.microsoft_translation_url)