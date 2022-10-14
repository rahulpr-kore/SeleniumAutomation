# Selenium Automation

This is a utility for translating text in between languages. The utility has support for breaking excel files into chunks, translating and then recombining and supports batch processing for multiple files in the folder.

### Installing dependencies:
Before you run the  `main.py`   script make sure to install all your python dependencies in the `requirements.txt` file. 

Make sure you introduce a language key in `.env`  file to your target lang if its absent from the  `env`  file in the path:

			Root
			└─── WebUtil
			    └─── env

### Running the script:
The script  `main.py`  is the entry point for the utility.  Just place you files in  `Test/chunks`  folder and you'll get the outputs in for all the excel files inside `chunks` in the `Test/chunks/Completed` folder.

		├───Test
		│   └───chunks    -> `Place your files in this folder`
		│       ├───Completed  -> `This is where you'll get your outputs`

### Credits
***************************************************************************************
This utility has been written by Rahul Kumar Prajapati and is for Kore internal use only. Kindly do not distribute it in any way shape or form.

*******************************************************************************************************
