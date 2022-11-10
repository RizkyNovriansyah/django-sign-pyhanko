from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
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
from django.http import FileResponse
from wsgiref.util import FileWrapper
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def sign(request):

    nik = request.POST['nik']
    passphrase = request.POST['passphrase']
    print("nik",nik)
    print("passphrase",passphrase)
    if nik == "11122233" and passphrase == "testing":
        pass
    else:
        return Response({'msg': 'NIK atau PASSPHRASE anda salah'}, status=status.HTTP_400_BAD_REQUEST)

    if request.FILES:
        if 'file' in request.FILES:
            file = request.FILES['file']
            reason = request.POST['reason']
            reason = request.POST['reason']
            
            print(file)
            model_created = SignModel.objects.create(file=file)
            sign_proceess(model_created,reason)
            short_report = open(model_created.file.path, 'rb')
            response = HttpResponse(FileWrapper(short_report), content_type='application/pdf')
            # return  Response({"id":model_created.id, "model_created_path":model_created.file.path})
            # return Response(response)
            short_report = open(model_created.file.path, 'rb')
            response = HttpResponse(FileWrapper(short_report), content_type='application/pdf')

            # img = open(model_created.file.path, 'rb')

            # response = JsonResponse(img)
            # return response
            # return FileResponse(open(model_created.file.path, 'rb'), content_type='application/pdf')
            # response = HttpResponse(model_created.file.read())
            # response['Content-Disposition'] = 'filename=some_file.pdf'
            # return response

            return response
        else:
            return Response({'detail':'invalid key!'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'detail': 'file is missing!'}, status=status.HTTP_400_BAD_REQUEST)

def sign_proceess(obj,reason):
    time_stamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    with open(obj.file.path, 'rb+') as doc:
        w = IncrementalPdfFileWriter(doc)
        append_signature_field(w, SigFieldSpec(sig_field_name="Coofis Sign:"+reason+" ("+time_stamp+")"))
        w.write_in_place()
    return 