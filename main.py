from WebUtil.translatecore import TranslateCore

obj = TranslateCore(use_edge=False, use_headless=True)
# translations = obj.translate_text_to_lang(use_single_service=False, translation_lang_key="EN")
obj.process_excel(filepath=r"./Test/ARB Arabic Demo NonSA-analysis-failintent.csv", \
                    outputpath=r"./Test/Output_ARB_Arabic_Demo_NonSA-analysis-failintent.xlsx")
# print(translations)