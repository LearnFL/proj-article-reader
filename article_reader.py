from pathlib import Path
import re
import os
from threading import Thread, Lock

from PyPDF2 import PdfReader



class CountMissing:
    def __init__(self):
        self.count_missing = 0
        self.count = 0
        self.aList = []

    def missing(self, file):
        self.count_missing += 1
        self.aList.append(file)
    
    def count_pdf(self):
        self.count += 1

    def report(self):
        return f'Total read: {self.count}, total could not read: {self.count_missing}, files could not read by name: {self.aList}'
    
pdf_report= CountMissing()

class InputClass:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.lock = Lock()
        self.failed = []

    def read(self):
        with self.lock:
            try: 
                with open(self.pdf_file, 'rb') as f:
                    pdf = PdfReader(f)
                    pages = pdf.pages
                    for idx, page in enumerate(pages, 1):
                        yield (len(pages), idx, self.pdf_file, page)
            except:
                yield None

    @classmethod
    def generate_inputs(cls, data_dir):
        for file in os.listdir(data_dir):
            head, tail = os.path.split(file)
            if Path(tail).suffix == '.pdf':
                yield cls(os.path.join(data_dir, file))


        
class PdfSearch:
    def __init__(self, input, pattern, to_txt, grab_extra, params, print_on_screen):
        self.input = input
        self.report = []
        self.lock = Lock()
        self.pattern = pattern
        self.grab_extra = grab_extra
        self.to_txt = to_txt
        self.params = params
        self.print_on_screen = print_on_screen

    def dump_txt(self):
        with self.lock:
            if self.to_txt:
                with open(os.path.join(self.to_txt), "a") as writer:
                    for entry in self.report:
                        writer.write(f'{entry} \n\n')

    def present_data(self, pattern):    
        if self.input.read() == None or None in self.input.read():
            pdf_report.missing(self.input.pdf_file)
            return
        
        with self.lock:
            pdf_report.count_pdf()  

        for pagesN, idx, file_name, page in self.input.read():
            result = pattern.finditer(page.extract_text())
            for i in result:
                if self.grab_extra == 0:
                    self.report.append(f'File Name: {file_name}, Page: {idx} of {pagesN}, {i.group()}')
                    if self.print_on_screen:
                        print(f'File Name: {file_name}, Page: {idx} of {pagesN}, {i.group()}')
                    
                if self.grab_extra > 0:
                    try:
                        self.report.append(f'File Name: {file_name}, Page: {idx} of {pagesN}, {page.extract_text()[i.start()-self.grab_extra : i.end()+self.grab_extra]}')
                        if self.print_on_screen:
                            print(f'File Name: {file_name}, Page: {idx} of {pagesN}, {page.extract_text()[i.start()-self.grab_extra : i.end()+self.grab_extra]}')
                    except:
                        self.report.append(f'File Name: {file_name}, Page: {idx} of {pagesN}, {i.group()}')
                        if self.print_on_screen:
                            print(f'File Name: {file_name}, Page: {idx} out of {pagesN}, {i.group()}')

            self.dump_txt()

    def build_patterns(self):
        include = ''.join([f"(?=.*\\b{i}\\b.*)" for i in params.get('include', '')])
        exclude = ''.join([f"(?!.*\\b{i}\\b.*)" for i in params.get('exclude', '')]) 
        keywords = '|'.join([f'\\b{i}\\b' for i in params.get('keywords', '')])
        pattern = r""+include+exclude+".*("+keywords+").*"    
        return pattern
    
    def filter(self):
        if self.pattern != None:
            pattern = re.compile(self.pattern, re.IGNORECASE)
            self.present_data(pattern)
        elif self.params != None:
            pattern = re.compile(self.build_patterns(), re.IGNORECASE)
            self.present_data(pattern)
            
    @classmethod
    def build_workers(cls, data_dir, input_class, pattern, grab_extra, to_txt, params, print_on_screen):
        workers = []
        for input_data in input_class.generate_inputs(data_dir):
            workers.append(cls(input_data, pattern, to_txt, grab_extra, params, print_on_screen))
        return workers



def execute(workers):
    print('Reading files, it may take a minute...')
    
    threads = [Thread(target=w.filter) for w in workers]    
    for thread in threads: thread.start()
    for thread in threads: thread.join()
      
    print(pdf_report.report())


 
def search_pdf(data_dir, *, params=None, pattern=None, to_txt=None, worker_class=PdfSearch, input_class=InputClass, grab_extra=0, print_on_screen=True):

    if not os.path.exists(data_dir):
        raise IOError(f"{data_dir}: Invalid input destination. Select a diferent destination.")
    
    head, tail = os.path.split(to_txt)
    if Path(tail).suffix != '.txt':
        to_txt = os.path.join(to_txt, "report.txt")

    if not isinstance(grab_extra, int) or grab_extra < 0:
        raise ValueError('grab_extra: must provide integer greater than 0.')

    workers = worker_class.build_workers(data_dir, input_class, pattern, grab_extra, to_txt, params, print_on_screen)
    return execute(workers)


'''

EXAMPLE:

dir_path = Path(r'SOME PATH')
save_dir = os.path.join(dir_path, 'my_report.txt')
pattern = r'\w{1}'

search_pdf(dir_path, to_txt=save_dir, pattern=pattern, grab_extra=10)

'''
