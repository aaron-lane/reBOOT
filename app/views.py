# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery.result import AsyncResult
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .forms import DocumentForm
from .tasks import parser
from .tasks import generate_pdf
from django.views.decorators.csrf import csrf_exempt
from celery.result import AsyncResult
from django.core.urlresolvers import reverse
import csv
import json
import zipfile


# Create your views here.
def get_csv(request):
    '''
    A view to redirect after task queuing csv parser
    '''
    if 'job' in request.GET:
        job_id = request.GET['job']
        job = AsyncResult(job_id)
        data = job.result or job.state
        context = {
            'data': data,
            'task_id': job_id,
        }
        return render(request, "app/CSVworked.html", context)
    elif (request.method == 'POST'):
        csv_file = request.FILES.get('my_file', False)
        if(csv_file and csv_file.name.endswith('.csv')):
            job = parser.delay(csv_file)
            return HttpResponseRedirect(reverse('get_csv') + '?job=' + job.id)
        else:
            return render(request, 'app/CSVfailed.html')
    else:
        return HttpResponseRedirect('/')


def poll_state(request):
    '''
    A view to report the progress to the user
    '''

    data = 'Fail'
    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
            data = task.result or task.state
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an AJAX request'

    try:
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')
    except:
        return HttpResponse(data, content_type='application/force-download')

def start_pdf_gen(request):
    if 'job' in request.GET:
        job_id = request.GET['job']
        job = AsyncResult(job_id)
        data = job.result or job.state
        context = {
            'data': data,
            'task_id': job_id,
        }
        print(job.state)
        # if(data == "PENDING"):
        #     return HttpResponse(job, content_type='application/zip')
        return render(request, "app/CSVworked.html", context)
    elif (request.method == 'POST'):
            job = generate_pdf.delay(request.queryset);
            return HttpResponseRedirect(reverse('start_pdf_gen') + '?job=' + job.id)
    else:
        return HttpResponseRedirect('/')
