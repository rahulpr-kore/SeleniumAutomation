from WebUtil.translatecore import TranslateCore
import pandas as pd
import os
import time
from tqdm import tqdm

def break_chunks(filepath=r"./Test/Benchmark_Banking77_train.xlsx"):
    df = None
    try:
       df = pd.read_excel(filepath)
    except:
        print("[INFO] File not read")
    rows_per_file = 1000

    n_chunks = len(df) // rows_per_file

    for i in range(n_chunks):
        start = i*rows_per_file
        stop = (i+1) * rows_per_file
        sub_df = df.iloc[start:stop]
        base_filename = "".join(filepath.split("/")).split(".")[-2]
        sub_df.to_excel(f"./Test/chunks/{base_filename}-{i}.xlsx", index=False)
    if stop < len(df):
        sub_df = df.iloc[stop:]
        sub_df.to_excel(f"./Test/chunks/{base_filename}-{i}.xlsx", index=False)

def merge_files(outputpath="./Test/Final_Output_Benchmark_Banking77_train.xlsx",\
                    chunk_path=r"./Test/chunks/"):

    filenames = os.listdir(chunk_path)
    output_df = None
    print(filenames)
    for idx, file in tqdm(enumerate(filenames), total=len(filenames)):
        if ".xlsx" not in file:
            continue
        print(file)
        if idx == 0:
            pd.read_excel(f"{chunk_path}{file}")
        df = pd.read_excel(f"{chunk_path}{file}")
        output_df = pd.concat([output_df, df], axis=0)
    output_df.to_excel(outputpath, index=False)

def process_folder(folder_name, return_dummy_for_google=True, \
                    translation_lang_key="EN", use_edge=False):
    file_list = os.listdir(folder_name)
    for file in file_list:
        if ".xlsx" not in file:
            continue
        print(f"[INFO] Processing file {file}")
        obj = TranslateCore(use_edge=use_edge, use_headless=False)
        obj.process_excel(filepath=f"./Test/chunks/{file}", \
                            outputpath=f"./Test/chunks/Completed/Output_{file}", \
                                translation_lang_key=translation_lang_key, \
                                    return_dummy_for_google=return_dummy_for_google)
        #Uncomment for multiple files so that you bypass Microsoft 2Mil limit
        time.sleep(15 * 60)


if __name__ == '__main__':
    #For breaking files in chunks if you've got a big excel file might be a good idea
    # break_chunks(filepath=r'./Test/YOUR_FILE_NAME.xlsx')

    #For translation batch processing
    process_folder("./Test/chunks", return_dummy_for_google=False, \
        translation_lang_key="FR", use_edge=False)

    #For Merging all excelfiles inside completed folder
    # merge_files(outputpath="./Test/Final_Output_Benchmark_Banking77_train.xlsx",\
    #             chunk_path=r"./Test/chunks/Completed/")