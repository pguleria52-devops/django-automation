from django.shortcuts import render,redirect
from .utils import get_all_custom_models
from uploads.models import Upload
from django.conf import settings
from django.core.management import call_command
import os
from django.contrib.messages import constants as messages

# Create your views here.
def import_data(request):
    if request.method == 'POST':    
        file_path = request.FILES.get('file-path')
        model_name = request.POST.get('model_name')

        #store the file in upload model
        upload = Upload.objects.create(file= file_path, model_name = model_name)
        
        # construct the full path
        relative_path = upload.file.path #in video it is url
        base_url = settings.BASE_DIR
        file_path = os.path.join(base_url, relative_path)

        #trigger the imnport data command
        # try:
        #     call_command('importdata',file_path, model_name)
        #     messages.success(request, 'Data imported succesfully')
        # except Exception as e:
        #     messages.error(request, str(e))    
        return redirect('import-data')

    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models': custom_models,
        } 
    return render(request, 'dataentry/importdata.html',context)