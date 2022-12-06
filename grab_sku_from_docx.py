import docx2txt
import re

# grab the text from extracted_docx\\word\\document.xml

def grab_sku_from_docx(docx_file_name):
    # use docx2txt to extract the text from the docx file
    text = docx2txt.process(f'{docx_file_name}.docx')
    print(text)

    # # use a regular expression to find anything between <w:t> and </w:t>
    # import re
    # text = re.findall('<w:t>(.*?)</w:t>', text)
    # print('grabbed text', text)
    # # join them all into one big string
    # text = ' '.join(text)
    # print("joined text", text)

    # use a regular expression to make a list of any numbers of length 9
    text = re.findall('\d{9}', text)
    print('grabbed upcs', text)
    return text

# test it out
if __name__ == '__main__':
    grab_sku_from_docx('test')