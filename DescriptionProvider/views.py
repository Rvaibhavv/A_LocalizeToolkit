from django.shortcuts import render,redirect
from .forms import FileUploadForm
from .models import UploadedFile

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

                return render(request,'DescriptionProvider/index.html')

    return render(request,'DescriptionProvider/index.html', {'form': form})
# Create your views here.
