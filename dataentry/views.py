from django.shortcuts import render, redirect
from .utils import check_csv_errors, get_all_custom_models
from uploads.models import Upload
from django.conf import settings
from .tasks import import_data_task, export_data_task
from django.contrib import messages  # Fixed import
from django.core.management import call_command

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

        #check for errors
        try:
            check_csv_errors(actual_file_path,model_name)
        except Exception as e:
            messages.error(request, str(e))  
            return redirect('import-data')  
        # Trigger the import data command
        import_data_task.delay(actual_file_path,model_name)

        #show output messages
        messages.success(request, 'Your data is being imported and will be notified once done.')
        
        return redirect('import-data')

    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models': custom_models,
        } 
        return render(request, 'dataentry/importdata.html', context)
    
def export_data(request):
    if request.method == 'POST':
        model_name = request.POST.get('model_name')

        #call the export data task
        export_data_task.delay(model_name)

        #show the message to the user
        messages.success(request, 'Your data is being Exported')
        return redirect('export-data')
    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models': custom_models
        }
    return render(request, 'dataentry/exportdata.html', context)    