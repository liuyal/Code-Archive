import os, sys, time, datetime, re
import PyPDF2

from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def extract_B(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums): interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    return text


def extract_A(path):
    pdfFileObj = open(path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    number_of_pages = pdfReader.numPages
    pages = []
    for i in range(0, number_of_pages): pages.append(pdfReader.getPage(i).extractText())
    return pages


def parser(pages):
    text_parsed = []
    for page in pages:
        for item in year_list: page = page.replace(str(item), "\n\n" + str(item))
        for item in keywords_list_A: page = page.replace(item, item + "\n")
        for item in keywords_list_B: page = page.replace(item, "\n" + item)
        for item in keywords_list_C: page = page.replace(item, "\n" + item + " ")
        for item in space_list: page = page.replace(item, " " + item)
        for item in double_list: page = page.replace(item, "\n\n" + item)
        page = page.replace("C\n", "C")
        page = page.replace("MACM \n\n", "MACM ")
        page = page.replace("END OF UNDERGRADUATE CAREER", "\n\n******************* END OF UNDERGRADUATE CAREER *******************\n\n")
        page = page.replace("End of Report", "\n\n******************* End of Report *******************")
        text_parsed.append(page)

    return text_parsed


def organizer(text):
    start_index = text.index("Program:BASC Engineering Science")
    middle_index = text.index("TOTAL UNITS PASSED BY ACADEMIC GROUP")
    end_index = text.index("END OF UNDERGRADUATE CAREER")

    class_section = text[start_index:middle_index]
    total_section = text[middle_index:end_index]

    class_section_lines = [x for x in class_section.split("\n") if "SFUSR550" not in x and "ADVISING TRANSCRIPT" not in x and len(x) > 1 and "***" not in x]

    result = []
    term_gpa = []
    cgpa = []
    semester = ""
    for item in class_section_lines:
        if "20" in item and ("Fall" in item or "Spring" in item or "Summer" in item):
            result.append(item.split("Good")[0])
            semester = item.split("Good")[0]
        elif item.split(" ")[0] in keywords_list_C:
            subject = item.split(" ")[0]
            number = item.split(" ")[1][0:item.split(" ")[1].index(".") - 1]
            credit = item.split(" ")[1][item.split(" ")[1].index(".") - 1:item.split(" ")[1].index(".") + 2]
            grade = ''.join([i for i in item.split(" ")[1].replace(".", "") if not i.isdigit()]).replace("W", "")
            GP = item.split(" ")[1][item.split(" ")[1].index(grade):-1].replace("P", "").replace("A", "").replace("B", "").replace("C", "").replace("+", "").replace("-", "")
            if grade == "": grade = "*"; GP = "0.00"
            result.append("\t" + subject + " " + number + "\t" + credit + "\t" + grade + "\t" + GP)

        elif "Term" in item:
            term_gpa.append(semester + "\tTerm GPA" + "\t" + item[item.index("(") + 1:item.index(")")].replace(" ", "") + "\t" + item.split(")")[-1])

        elif "CGPA" in item:
            cgpa.append(semester + "\tCGPA" + "\t" + item[item.index("(") + 1:item.index(")")].replace(" ", "") + "\t" + item.split(")")[-1])

    f = open("transcript_parsed.csv", "a+")
    f.truncate(0)
    f.write("\n".join(result))
    f.close()

    f = open("term_gpa.csv", "a+")
    f.truncate(0)
    f.write("\n".join(term_gpa))
    f.close()

    f = open("cgpa.csv", "a+")
    f.truncate(0)
    f.write("\n".join(cgpa))
    f.close()

    data = {}
    year = ""
    for item in result:
        if '\t' not in item:
            year = item
        else:
            class_name = item.split('\t')[1]
            class_credit_count = item.split('\t')[2]
            class_letter_grade = item.split('\t')[3]
            class_grade_point = item.split('\t')[4]

            if class_name not in list(data.keys()): data[class_name] = {}

            data[class_name]["year"] = year
            data[class_name]["level"] = int(class_name.split(' ')[-1][0]) * 100
            data[class_name]["credit_count"] = class_credit_count
            data[class_name]["letter_grade"] = class_letter_grade
            data[class_name]["grade_point"] = class_grade_point

    return data


def ud_gpa_calculator(data, level):

    classes = []

    for item in data:
        if int(data[item]["level"]) == int(level):
            classes.append(data[item])

    for item in classes


    return 0


if __name__ == "__main__":
    year_list = range(2010, 2025)
    keywords_list_A = ["Secondary", "Good Academic Standing"]
    keywords_list_B = ["TRANSFER", "Term GPA", "CGPA", "CUDGPA", "UDGPA", "TOTAL UNITS PASSED", "STUDENT TOTALS", "Passed", "Points", "incl in GPA", "Cum.GPAs"]
    keywords_list_C = ["CMPT", "ENSC", "MATH", "PHYS", "CHEM", "BPK", "ECON", "IAT", "MACM", "EDUC", "APSC", "ARTS", "CAT", "SCI"]
    double_list = ["SFUSR550", "TOTAL UNITS PASSED BY ACADEMIC GROUP"]
    space_list = ["Good Academic Standing"]

    pages = extract_A(os.getcwd() + os.sep + "sfu.PDF")
    text_parsed = parser(pages)
    classes = organizer("".join(text_parsed))

    ud_gpa_calculator(classes, 400)
