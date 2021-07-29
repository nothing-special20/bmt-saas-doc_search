import re
import json
import sys
import os

import pytesseract
import pdf2image
from PIL import Image, ImageSequence
from elasticsearch import Elasticsearch, helpers

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.core.files.uploadedfile import TemporaryUploadedFile

from .models import MiscDocs

"""
    Function that loads files from a folder into elasticsearch
    Source: https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/
"""
def handle_uploaded_file(filename, image_list):
    # try:
    es = Elasticsearch()
    data = pdf_ocr(filename, image_list)
    for record in data:
        doc = MiscDocs(FILENAME=filename,
                        PG_NUM=record['PG_NUM'],
                        DOC_TEXT=record['DOC_TEXT'])
        doc.save()
        print(record)

"""
	Misc Text Cleaning
"""
def misc_cleaning(text):
	output = re.sub('\n', ' ', text)
	output = re.sub(' {2,250}', ' ', output)
	output = re.sub(r'[^\x00-\x7F]+',' ', output)
	return output


def get_image_list(open_object, filename):
    print(type(open_object))
    if type(open_object) is TemporaryUploadedFile:
        if '.tif' in filename:
            # img = Image.open(path) #.convert("RGBA")
            img = Image.from_bytes(open_object)
            image_list = []
            for page_num, page in enumerate(ImageSequence.Iterator(img)):
                image_list.append(page)
        else:
            try:
                image_list = pdf2image.convert_from_bytes(open_object.seek(0)) #.read()
            except:
                image_list = pdf2image.convert_from_path(open_object, fmt="jpeg")

    else:
        try:
            image_list = pdf2image.convert_from_bytes(open_object.read())
        except:
            image_list = pdf2image.convert_from_path(open_object, fmt="jpeg")


    return image_list
        

"""
	Check if file name matches regular expressions for recently downloaded file names

	:param doc - path to the pdf to feed into the OCR
"""
def pdf_ocr(filename, image_list):
    #Loop through individual pages
    txt = ''
    page_counter = 0
    all_pg_data = []
    for single_img in image_list:
        page_counter += 1
        try:
            single_pg_txt = pytesseract.image_to_string(single_img).encode("utf-8")
            single_pg_txt = str(single_pg_txt)
            single_pg_txt = single_pg_txt.lower()
            single_pg_txt = misc_cleaning(single_pg_txt)

            single_pg_details = {'FILENAME': filename,
                                'PG_NUM': str(page_counter),
                                'DOC_TEXT': single_pg_txt}

            all_pg_data.append(single_pg_details)

        except:
            pass

    return all_pg_data

"""
    Creates a GUI for a user to select files to upload from
"""
def gui_folder():
    layout = [[sg.Text('Root Path'), sg.InputText('', key='input_folder'), sg.FolderBrowse('Browse Folders'), sg.Button('Load Data!')]]
    window = sg.Window('File Search Engine').layout(layout)
    event, values = window.Read()
    if event == 'Load Data!':
        input_folder = values['input_folder']
        window.close()
    
    filelist = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            filelist.append(os.path.join(root,file))

    return filelist

"""
    Query elasticsearch
    params:    
        search_text - text to search for
"""
def es_query(search_text):
    try:
        data = {"_source": ["FILENAME", "PG_NUM", "DOC_TEXT"],
                    "size": 500, 
                    "query": {
                        "query_string": {
                            "query": search_text,
                            "phrase_slop": 0
                        }
                    } 
                }

        headers = {'Accept': 'application/json', 
                    'Content-type': 'application/json'}

        es = Elasticsearch()
        output = es.search(index='miscdocs', body=data)
        results = output['hits']['hits']
        files = [x['_source']['FILENAME'] for x in results]
        pg_nums = [x['_source']['PG_NUM'] for x in results]
        results = [{"FILENAME": x['_source']['FILENAME'],
                    "PG_NUM": x['_source']['PG_NUM'],
                    "DOC_TEXT": highlight(x['_source']["DOC_TEXT"], search_text) 
                    } for x in results]
    except:
        results = [{"FILENAME": "_", "PG_NUM": "_", "DOC_TEXT": "_"}]

    return results


"""Custom filters"""
register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter
def highlight(value, search_term, autoescape=True):
    # return mark_safe(value.replace(search_term, "<span class='highlight'>%s</span>" % search_term))
    return mark_safe(re.sub(search_term, '<strong>' + search_term + '</strong>', value))