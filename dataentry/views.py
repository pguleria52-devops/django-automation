from django.shortcuts import render, redirect
from .utils import get_all_custom_models
from uploads.models import Upload
from django.conf import settings
from django.core.management import call_command
import os
from django.contrib import messages  # Fixed import

def import_data(request):
    if request.method == 'POST':    
        file_path = request.FILES.get('file-path')
        model_name = request.POST.get('model_name')

        # Store the file in upload model
        upload = Upload.objects.create(file=file_path, model_name=model_name)
        
        # Get the actual file path (not URL)
        # upload.file.path gives the absolute path to the uploaded file
        actual_file_path = upload.file.path
        
        # Debug print (remove in production)
        print(f"File path: {actual_file_path}")
        print(f"Model name: {model_name}")

        # Trigger the import data command
        try:
            call_command('importdata', actual_file_path, model_name)
            messages.success(request, 'Data imported successfully')
        except Exception as e:
            messages.error(request, f'Error importing data: {str(e)}')
            print(f"Import error: {e}")  # For debugging
        
        return redirect('import-data')

    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models': custom_models,
        } 
        return render(request, 'dataentry/importdata.html', context)