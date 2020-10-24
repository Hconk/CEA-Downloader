# -*- coding:utf-8*-
# 利用PyPDF2模块合并同一文件夹下的所有PDF文件
# 只需修改存放PDF文件的文件夹变量：file_dir 和 输出文件名变量: outfile

import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import time
import requests
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open
import re
import getopt
import json
import sys

def download_pdf(start, end, url, path):
    file_url = "http://cea.ceaj.org/CN/article/downloadArticleFile.do?attachType=PDF&id="
    for i in range(start, end + 1):
        r = requests.get(file_url + str(i), stream=True)
        with open("{}/{}.pdf".format(path, i), "wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)

# 使用os模块的walk函数，搜索出指定目录下的全部PDF文件
# 获取同一目录下的所有PDF文件的绝对路径
def getFileName(filedir):

    file_list = [os.path.join(root, filespath) \
                 for root, dirs, files in os.walk(filedir) \
                 for filespath in files \
                 if str(filespath).endswith('pdf')
                 ]
    return file_list if file_list else []

# 合并同一目录下的所有PDF文件
def MergePDF(filepath, outfile):

    output = PdfFileWriter()
    outputPages = 0
    pdf_fileName = getFileName(filepath)

    if pdf_fileName:
        for pdf_file in pdf_fileName:
            print("路径：%s"%pdf_file)

            # 读取源PDF文件
            input = PdfFileReader(open(pdf_file, "rb"),strict=False)

            # 获得源PDF文件中页面总数
            pageCount = input.getNumPages()
            outputPages += pageCount
            print("页数：%d"%pageCount)

            # 分别将page添加到输出output中
            for iPage in range(pageCount):
                output.addPage(input.getPage(iPage))

        print("合并后的总页数:%d."%outputPages)
        # 写入到目标PDF文件
        outputStream = open(os.path.join(filepath, outfile), "wb")
        output.write(outputStream)
        outputStream.close()
        print("PDF文件合并完成！")

    else:
        print("没有可以合并的PDF文件！")


def add_bookmarks(pdf, bookmarks, offset):
    pdf_path = pdf
    page_offset = offset

    output_pdf = PdfFileWriter()

    input = PdfFileReader(open(pdf_path, "rb"),strict=False)
    pageCount = input.getNumPages()
    for i in range(pageCount):
        output_pdf.addPage(input.getPage(i))
    
    for name, page in bookmarks:
        page_num = page + offset - 1
        if page_num >= pageCount:
            break
        output_pdf.addBookmark(name, page_num)
    output_pdf_path = os.path.splitext(pdf_path)[0] + '-bookmarked.pdf'
    with open(output_pdf_path, 'wb') as pdf_file:
        output_pdf.write(pdf_file)
def read_pdf(pdf_file):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdf_file)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content

def get_bookmarks(pdf):
    pdf_file = open(pdf, 'rb')
    output_string = read_pdf(pdf_file)
    rx_all = re.compile('^(?!…)([\u4e00-\u9fa5]*.*[\u4e00-\u9fa5]+（\d*）)', re.MULTILINE)
    bookmark_txt = rx_all.finditer(output_string)
    book_json = []
    # for line in all_match
    for match in bookmark_txt:
        all_match = match.groups()[0].replace('）','')
        book_json.append([all_match.split('（')[0], int(all_match.split('（')[1])])
    return book_json

def usage():
    print(' -h help \n'\
          ' -s start 起始编号\n'
          ' -e end 终止编号\n'
          ' -o output 文件保存路径')
    exit(-1)

def opt_parser(args):
    try:
        start = 0
        end = 0
        output_file = ''
        options, args = getopt.getopt(args[1:], 'hs:e:o:', ['help', 'start=', 'end=', 'output='])
        for name, value in options:
            if name in ('-h', '--help'):
                usage()
            elif name in ('-s', '--start'):
                start = value
            elif name in ('-e', '--end'):
                end = value
            elif name in ('-o', '--output'):
                output_file = value
        return (start, end, output_file)
    except getopt.GetoptError:
        usage()
    else:
        usage()
                


# 主函数
def main():
    start, end, path = opt_parser(sys.argv)
    start = int(start)
    end = int(end)
    if not os.path.exists(path):
        os.makedirs(path)
    download_pdf(start, end, "", path)
    MergePDF(path,"merge_all.pdf")
    book_marks = get_bookmarks(path + "/{}.pdf".format(start))
    add_bookmarks(path + "/merge_all.pdf", book_marks, 5)

if __name__ == "__main__":
    main()