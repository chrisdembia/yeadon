'''This function takes in a PDF form of yeadon measurements and produces an
input txt file formidable for use with the yeadon package.

Usage: at a bash command prompt, type

    python measpdf2txt.py <pdffname> <txtname>

where <pdffname> is the name of a measurement PDF form, such as measform.pdf
and <txtname> is the name of the output text file, such as output.txt.

Dependencies:

    python2.4+
    pdfminer python package

Contact C. Dembia fitzeq@gmail.com with questions.

'''
import sys
from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdftypes import resolve1

filename = sys.argv[1]
fp = open(filename, 'rb')
parser = PDFParser(fp)
doc = PDFDocument()
parser.set_document(doc)
doc.set_parser(parser)
doc.initialize('')

fo = open(sys.argv[2], 'w')

fields = resolve1(doc.catalog['AcroForm'])['Fields']

ctr = 0
for i in fields:
    ctr = ctr + 1
    field = resolve1(i)
    name, value = resolve1(field.get('T')), resolve1(field.get('V'))
    print '{0}: {1}'.format(name, value[3::])
    if name != 'Name' and name != 'Date':
        if value == '':
            print "Value for the field",name,"is empty! Not okay!"
            raise Exception()
        tempstr = ''
        c = 0
        for j in value[3::]:
            c = c + 1
            if c % 2 == 1:
                tempstr = tempstr + j
        fo.write('{0}={1}\n'.format(name,float(tempstr)))

fp.close()
fo.close()
