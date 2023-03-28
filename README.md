# Multiple PDF files reader

### Disclaimer
This project is a work in progress and was designed to accomplish a specific task. At the moment, this script functions as intended, but since this is the first version, there will be multiple modifications and bug fixes made over time. I welcome any constructive feedback and suggestions to help improve this project.

### Description
This script allows you to quickly and easily search multiple PDF files located in a single folder. You can specify search parameters such as keywords, must-contain words, must-not-contain words. The script will then build a <b>BASIC</b> regular expression style pattern to search the PDFs, or you may submit your own pattern instead. Results can be printed on screen and/or saved to a file. This is a great tool for quickly finding the information you need from multiple PDFs.   

### How to use
You may submit a dictionary with keywords along with their associated values. The values must be in the form of a list: <br><br>
<b>include</b>: must contain words<br>
<b>exclude</b>: must not contain words<br>
<b>keywords</b>: list of keywords<br>

<br>
Passing all three keys is not a requirement. You can choose to pass only one or two of the keys if that works better for you. This gives you the flexibility to customize your experience and pick the keys that are most important to you.<br><br>

```
params = {
        'include':['Al'], 
        'exclude': ['cathode'], 
        'keywords':['ion']
         }
         
search_pdf('c:/my_folder_with_pdf', params=params)
```
<br>
Using Regular Expressions style patterns, you can pass your own unique pattern to search for specific text in a PDF. : <br><br>

```
my_pattern = "(?=.*mobility).*"

search_pdf('c:/my_folder_with_pdf', pattern=my_pattern)
```

### Optional parameters
<b>to_txt</b> takes a path where you want to save a text file that contains findings including file name and page on which finding is present.<br><br>
<b>to_csv</b> takes a path where you want to save a csv file that contains findings including file name and page on which finding is present.<br><br>
<b>to_excel</b> takes a path where you want to save an excel file that contains findings including file name and page on which finding is present.<br><br>
<b>grab_extra</b> takes a postive integer that specifies a number of charechters before and after the finding that you want to include and add to the finding.<br><br>
<b>print_on_screen</b> the default is True, prints result in terminal, that includes file name and path, page number where the finding is present and the finding itself.<br><br>

```
my_pattern = "SOME PATTERN"

search_pdf('c:/my_folder_with_pdf', to_text="c:/some_path/my_text_file.txt", pattern=my_pattern, 
            grab_extra=25, print_on_screen=True)
```

### Example of output:
#### Screen
```
Reading files, it may take a minute...
File Name: C:\Users\..\Articles\368635591.pdf, Page: 64 of 290, crystals 
cooled too quickly exhibit thermal strain and crack easily.26  Fast cooling of
File Name: C:\Users\..\Articles\268634785.pdf, Page: 144 of 290, limiting the suitable crystal growth techniques.  Because of this complication as well as additional problems with thermally-induced cracking and continued problems 
File Name: C:\Users\...\Articles\Articles\768635545.pdf, Page: 173 of 290, LiB 6O10 (CLBO) which is severely hygroscopic and tends to crack.16  A more advanced 
study
Total read: 8, Found: 212, total could not read: 1, files could not read by name: ["C:\\Users\\...\\Articles\\report356.pdf"]
```
#### Text file
<img width="308" alt="text" src="https://user-images.githubusercontent.com/86169204/228311462-09697381-84cb-448a-9b38-97e635d469d3.PNG">

#### CSV
<img width="482" alt="csv" src="https://user-images.githubusercontent.com/86169204/228311173-faebc08d-c37b-4e36-be05-888980c8cb67.PNG">

#### EXCEL
<img width="660" alt="excel" src="https://user-images.githubusercontent.com/86169204/228310802-3c33cc25-2797-4cb0-be76-214a8e713f3b.PNG">

### Requirements
```
openpyxl==3.1.1
pandas==1.5.3
PyPDF2==3.0.1
```
