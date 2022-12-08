import docx2txt
import re

# grab the text from extracted_docx\\word\\document.xml

def grab_sku_from_docx(docx_file_name:str) -> str:
    # use docx2txt to extract the text from the docx file
    text = docx2txt.process(f'{docx_file_name}.docx')
    print(text)
    # use a regular expression to make a list of any numbers of length 9
    text = re.findall('\d{8,9}', text)
    print('grabbed upcs', text)
    return text[0]

# test it out
if __name__ == '__main__':
    grab_sku_from_docx('test')