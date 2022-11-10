from django.shortcuts import render
from django.http import HttpResponse
import subprocess
from .models import SignModel
from pyhanko.sign import signers
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign.fields import SigFieldSpec, append_signature_field
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import fields
import datetime
# Create your views here.
def index(request):
    
    with open('/home/linuxlite/Music/coba.pdf', 'rb+') as doc:
        w = IncrementalPdfFileWriter(doc)
        append_signature_field(w, SigFieldSpec(sig_field_name="Coofis Sign",doc_mdp_update_value=fields.MDPPerm.ANNOTATE))
        w.write_in_place()
    return HttpResponse("Hello, world. You're at the polls index.")
    # return render(request, 'main/main.html', locals())

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (api_view, permission_classes)
from wsgiref.util import FileWrapper
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def sign(request):
   
    if request.FILES:
        if 'file' in request.FILES:
            file = request.FILES['file']
            reason = request.POST['reason']
            print(file)
            model_created = SignModel.objects.create(file=file)
            sign_proceess(model_created,reason)
            short_report = open(model_created.file.path, 'rb')
            response = HttpResponse(FileWrapper(short_report), content_type='application/pdf')
            # return  Response({"id":model_created.id, "model_created_path":model_created.file.path})
            return response
        else:
            return Response({'detail':'invalid key!'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'detail': 'file is missing!'}, status=status.HTTP_400_BAD_REQUEST)

def sign_proceess(obj,reason):
    print(str(datetime.datetime.now()))
    with open(obj.file.path, 'rb+') as doc:
        w = IncrementalPdfFileWriter(doc)
        append_signature_field(w, SigFieldSpec(sig_field_name="Coofis Sign:"+reason+" "))
        w.write_in_place()
    return 