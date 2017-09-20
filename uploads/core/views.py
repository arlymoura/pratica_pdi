from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from uploads.core.models import Document
from uploads.core.forms import DocumentForm
import cv2
import numpy
import numpy as np
from PIL import Image
import urllib
from scipy.misc import imread, imsave
import os
import sys
import math

import argparse



def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', { 'documents': documents })


def simple_upload(request):

    if request.method == 'POST' and request.FILES['myfile']:
        print request.POST
        try:
            os.remove('media/entrada.png')
            os.remove('media/saida.png')
        except OSError, e:  ## if failed, report it back to the user ##
            pass

        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save('entrada.png', myfile)
        uploaded_file_url = fs.url(filename)
        image_out = imread(myfile).astype(np.float32)
        # image_out = loggray2(image_out, None,10)
        image_out = select_function(image_out, int(request.POST['func_select']), request)

        imsave('media/saida.png', image_out)
        image_out = fs.url('saida.png')

        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'image_out': image_out
        })
    return render(request, 'core/simple_upload.html')


def lingray(x, a=None, b=None):

 if a == None:
         a = np.min(x)
 if b == None:
         b = np.max(x)
 return 255.0 * (x-float(a))/(b-a)


def loggray2(x, a=None, b=None):

 if a == None:
         a = np.min(x)
 if b == None:
         b = np.max(x)
 linval = 10.0 + 990.0 * (x-float(a))/(b-a)
 return (np.log10(linval)-1.0)*0.5 * 255.0



def select_function(img, func, params):
    if func == 1:
        return loggray2(img,  int(params.POST['constant_1']), None)
    if func == 2:
        return loggray2(img, None, int(params.POST['constant_2']))

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })
