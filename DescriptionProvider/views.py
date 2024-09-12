from django.shortcuts import render,redirect
from .forms import FileUploadForm
from .models import UploadedFile
from django.contrib import messages
import os
from google.generativeai import text
from django.conf import settings

def index(request):
    form =FileUploadForm()

    if request.method =='POST':
        action =request.POST.get('action')

        if action =='describe' and request.FILES:
            form =FileUploadForm(request.POST,request.FILES)
            if form.is_valid():
                uploaded_file =form.cleaned_data['file']
                file_instance =UploadedFile(file=uploaded_file)
                file_instance.save()
                messages.success(request,'file uploaded sucessfully')

                file_instance_1 =UploadedFile.objects.last()
                if file_instance_1:
                    file_path =file_instance_1.file.path
                    if not os.path.exists(file_path):
                        return render(request,'DescriptionProvider/index.html',{'error':'file not found'})

                try:
                    with open(file_path,'r',encoding='utf-8') as file:
                        file_content =file.read()
                    prompt =file_content+'describe the following code'
                    client =text.TextServiceClient(api_key=settings.GEMINI_API_KEY)
                    response =client.generate_text(
                        model ='models/text-bison-001',
                        prompt = prompt,
                    )
                    return render(request,'DescriptionProvider/index.html',{'response':response.text})

                except Exception as e:
                    return render(request, 'DescriptionProvider/index.html', {
                    'error': f'Error during file processing: {str(e)}'
                })
    return render(request,'DescriptionProvider/index.html', {'form': form})
# Create your views here.
