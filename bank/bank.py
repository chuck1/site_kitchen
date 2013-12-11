import sys
import pyPdf
import os
import string

def getPDFContent(path):
    content = ""
    # Load PDF into pyPDF
    pdf = pyPdf.PdfFileReader(file(path, "rb"))
    # Iterate pages
    for i in range(0, pdf.getNumPages()):
        # Extract text from page and add to content
        content += pdf.getPage(i).extractText() + " \n"
    # Collapse whitespace
    #content = u" ".join(content.replace(u"\xa0", u" ").strip().split())
    
    return content

os.chdir(os.getcwd()+"/statements/old")
for files in os.listdir("."):
    if files.endswith(".cgi"):
        print files
        
        f = open(os.getcwd()+"/text/"+string.replace(files,".cgi",".txt"),'w+')
        f.write(getPDFContent(files))
        f.close()

raw_input("Press enter")
