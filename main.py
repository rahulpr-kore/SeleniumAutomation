from WebUtil.translatecore import TranslateCore

obj = TranslateCore(use_edge=False, use_headless=False)
# translations = obj.translate_text_to_lang(use_single_service=False, translation_lang_key="EN")
obj.process_excel(filepath=r"./Test/ARB Arabic Demo NonSA-analysis-failintent.csv", \
                    outputpath=r"./Test/TestOutput.xlsx", translation_lang_key="FR")
# print(translations)