import os

import django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string

from django.utils.html import conditional_escape

from django.db import models

from django.views.generic.edit import FormView

from .forms import FileFieldForm, UploadFileForm, DocumentForm
from .functions import handle_uploaded_file, misc_cleaning, pdf_ocr, es_query, get_image_list

# Create your views here.

def upload_file(request):
    form = UploadFileForm(request.POST, request.FILES)
    return render(request, 'search/upload_failure.html', {'form': form})
    if form.is_valid():
        handle_uploaded_file(request.FILES['file'])
        # return HttpResponseRedirect('/success/url/')
        return render(request, 'search/upload_success.html', {'form': form})
    else:
        return render(request, 'search/upload_failure.html', {'form': form})

"""
    Queries elasticsearch for search terms
"""
def search_page(request):
    search_text = "__"
    # if request.method == 'POST' and 'load-docs' in request.POST:
    if request.method == 'POST' and 'search-text' in request.POST:
        print('search-text')
        search_text = request.POST.get('search-text')

        return render(request, 'search/search_orig.html', 
                        {'es_files': es_query(search_text),
                        'upload_msg': '_____'})

    if request.method == 'POST' and len(request.FILES.getlist('load-docs'))>0:
        files_to_upload = request.FILES.getlist('load-docs')
        upload_counter = 0
        for x in files_to_upload:
            upload_counter += 1
            upload_msg = 'Uploading document ' + str(upload_counter) + ' of ' + str(len(files_to_upload))
            print(upload_msg + "\t" + str(x))
            request.POST.get('upload_msg', upload_msg + '\t' + str(x))

            handle_uploaded_file(str(x), get_image_list(x, str(x)))
        
        return render(request, 'search/search_orig.html', 
                                {'es_files': es_query(search_text),
                                'upload_msg': 'File upload finished!!'})


    else:    
        return render(request, 'search/search_orig.html', 
                                {'es_files': es_query(search_text),
                                'upload_msg': '_____'})

