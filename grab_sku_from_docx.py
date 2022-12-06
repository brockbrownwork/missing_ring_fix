# grab the text from extracted_docx\\word\\document.xml

with open("extracted_docx\\word\\document.xml", 'r') as f:
    text = f.read()
print(text)

# use a regular expression to find anything between <w:t> and </w:t>
import re
text = re.findall('<w:t>(.*?)</w:t>', text)

# join them all into one big string
text = ' '.join(text)

# use a regular expression to make a list of any numbers of length 9
import re
text = re.findall('\d{9}', text)
print(text)