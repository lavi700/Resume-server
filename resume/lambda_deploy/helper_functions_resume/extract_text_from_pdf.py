import PyPDF2

def extract_text_from_pdf(pdf_file_object):
    words_list = []
    pdfReader = PyPDF2.PdfReader(pdf_file_object)
    print(type(pdfReader))

    for page in pdfReader.pages:
        print(type(page))
        page_text = page.extract_text()
        print(22222222222222)
        print("page_text: ", page_text)
        if page_text:  # Check if page_text is not None
            for line in page_text.split('\n'):
                print("line: ", line)
                words_list.append(line)
                   
    return " ".join(words_list)

# def extract_text_from_pdf(pdfpath):
#     words_list = []
#     pdfFileObj = open(pdfpath, 'rb')
#     pdfReader = PyPDF2.PdfReader(pdfFileObj)

#     for index in range(len(pdfReader.pages)):
#         pageObj = pdfReader.pages[index]
#         page_text = pageObj.extract_text()
#         for line in page_text.split('\n'):  
#             words_list.append(line)
#     return " ".join(words_list)