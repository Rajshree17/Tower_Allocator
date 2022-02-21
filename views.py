from unicodedata import name
from urllib import response
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import Document
from django.conf import settings
from .forms import DocumentForm
import os
import sys


sys.path.insert(1, '/tower_allocator')

import tower_distance




def index(request):
    message = ''
    # Handle file upload
    if request.method == 'POST':
        
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
           
            
            folder = os.path.join(settings.MEDIA_ROOT,"documents")
            docfile = request.FILES['docfile']
            filename = request.FILES['docfile'].name
            final_file = tower_distance.get_closest_tower_data(f"{folder}\\{filename}")
        
            return redirect('index')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()  
  
    folder =os.path.join(settings.MEDIA_ROOT,"output")
    
    print(folder) 
    documents = os.listdir(folder)
 
    context = {'documents': documents, 'form': form, 'message': message}
  
    return render(request, 'Home/home.html',context)

def download(request,file):
    print("Hello_Test")
    file_path = f"media/output/{file}"
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path,'rb')as fh:
            response=HttpResponse(fh.read(),content_type="application/text")
            response['content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response
   
    raise Http404

    




    



