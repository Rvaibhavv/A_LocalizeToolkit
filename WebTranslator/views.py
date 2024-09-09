from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import UploadedFile
from googletrans import Translator
from bs4 import BeautifulSoup
import os
from django.conf import settings
translator = Translator()

def index(request): 
    form = FileUploadForm()
    
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'upload' and request.FILES:
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_file = form.cleaned_data['file']
                file_instance = UploadedFile(file=uploaded_file)
                file_instance.save()

                # Redirect to the language selection page
                return redirect('webtranslator:language')

    return render(request, 'WebTranslator/index.html', {'form': form})

def language(request):
    if request.method == 'POST':
        translate_lang = request.POST.get('action')
        dest_lang = translate_lang

        file_instance = UploadedFile.objects.last()

        if file_instance:
            file_path = file_instance.file.path
            if not os.path.exists(file_path):
                return render(request, 'WebTranslator/translate.html', {'error': 'File not found for translation.'})

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()

                soup = BeautifulSoup(html_content, 'html.parser')

                for element in soup.find_all(text=True):
                    original_text = element.strip()
                    if original_text:
                        translated_text = translator.translate(original_text, dest=dest_lang).text
                        element.replace_with(translated_text)

                translated_html_content = str(soup)
                
                translated_file_name = f'translated_html_{dest_lang}.html'
                translated_file_path = os.path.join(settings.MEDIA_ROOT, 'translated', translated_file_name)
                
                os.makedirs(os.path.dirname(translated_file_path), exist_ok=True)
                
                # Save the translated file
                with open(translated_file_path, 'w', encoding='utf-8') as file:
                    file.write(translated_html_content)

                # Prepare the download URL
                download_url = os.path.join(settings.MEDIA_URL, 'translated', translated_file_name)

                return render(request, 'WebTranslator/translate.html', {
                    'message': 'Translation complete!',
                    'download_url': download_url  # Pass the download URL to the template
                })

            except Exception as e:
                return render(request, 'WebTranslator/translate.html', {
                    'error': f'Error during translation: {str(e)}'
                })
        else:
            return render(request, 'WebTranslator/translate.html', {'error': 'No file uploaded to translate.'})

    return render(request, 'WebTranslator/translate.html')
