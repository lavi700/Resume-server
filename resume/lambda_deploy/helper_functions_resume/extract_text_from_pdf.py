import PyPDF2

def extract_text_from_pdf(pdfpath):
    words_list = []
    pdfFileObj = open(pdfpath, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    for index in range(len(pdfReader.pages)):
        pageObj = pdfReader.pages[index]
        page_text = pageObj.extract_text()
        for line in page_text.split('\n'):  
            words_list.append(line)
    return " ".join(words_list)