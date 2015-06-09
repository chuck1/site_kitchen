#! /usr/bin/env python

import sys
import pyPdf
import os
import string

from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

def get_text_1(path):
    input_ = file(path, 'rb')
    output = StringIO()

    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    process_pdf(manager, converter, input_)

    return output.getvalue() 

def get_text_2(path):
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

if __name__ == '__main__':

    d = "/home/chuck/Documents/bank/statements/old"

    print d

    for fn in os.listdir(d):
        if fn.endswith(".cgi"):
            print fn
           
            path = os.path.join(d, fn)

            fn_text = os.path.join(d, "text", string.replace(fn,".cgi",".txt"))

            text = get_text_1(path)

            with open(fn,'w+') as f:
                f.write(text)
                f.close()

            print text
    


