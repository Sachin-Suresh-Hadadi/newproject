from django.shortcuts import render
import boto3
import os,pathlib

# Create your views here.
def index(request):
    return render(request,'index.html')

def Create_Bucket(request):
    name=request.POST['bucket_name']
    res='not created'
    try:
        if request.POST:
            client = boto3.client(
                's3',
                 aws_access_key_id=os.getenv('ACCESSKEY'),
                 aws_secret_access_key=os.getenv('SECRETKEY'))
        AWS_REGION = "ap-south-1"
        location = {'LocationConstraint': AWS_REGION}
        response = client.create_bucket(Bucket=name, CreateBucketConfiguration=location)
        res='created'
        
    except Exception as e:
        res=type(e).__name__
    
    return render(request,'Create_Bucket.html',{'result':res})

def LIST_BUCKET(request):
    res={
        'buckets':[]
    }
    try:
        if 'list_bucket' in request.POST:
            AWS_REGION = "us-east-2"
            client = boto3.client("s3",aws_access_key_id=os.getenv('ACCESSKEY'),aws_secret_access_key=os.getenv('SECRETKEY') )
            response = client.list_buckets()
            for bucket in response['Buckets']:
                res['buckets'].append(bucket)
    except Exception as e:
        res=type(e).__name__
    return render(request,'LIST_BUCKET.html',{'result':res})

def Delete_Bucket(request):
    res='not deleted'
    name=request.POST['bucket_name']
    try:
        if 'Delete_bucket' in request.POST:
            client = boto3.client(
                    's3',
                    aws_access_key_id=os.getenv('ACCESSKEY'),
                    aws_secret_access_key=os.getenv('SECRETKEY'))
            AWS_REGION = "us-east-2"
            client.delete_bucket(Bucket=name)
            res='deleted'
            
    except Exception as e:
        res=type(e).__name__
        
    return render(request,'Delete_Bucket.html',{'result':res})

def Add_File(request):
    result='not uploaded'
    try:
        if 'ADD_FILE' in request.POST:
            bucket=request.POST['bucket_name_']
            BASE_DIR=request.post['file_path']
            file=request.POST['choosen_file']
            client = boto3.client(
                    's3',
                     aws_access_key_id=os.getenv('ACCESSKEY'),
                     aws_secret_access_key=os.getenv('SECRETKEY'))
            AWS_REGION = "us-east-2"
            def upload_files(file_name, bucket, object_name=None, args=None):
               if object_name is None:
                  object_name = file_name
               client.upload_file(f"{BASE_DIR}/{file}", bucket, object_name, ExtraArgs=args)
            upload_files(file,bucket)
            result='file added'
    except Exception as e:
        result=type(e).__name__
    return render(request,'Add_File.html',{'result':result})

def Delete_File(request):
    res='not deleted'
    try:
        if 'DELETE_FILE' in request.POST:
            bucket1=request.POST['bucket_name_']
            file=request.POST['choosen_file']
            s3= boto3.client('s3',
            aws_access_key_id=os.getenv('ACCESSKEY'),
            aws_secret_access_key=os.getenv('SECRETKEY')
            )
            response = s3.list_objects(Bucket=bucket1)
            objects=[]
            for item in response['Contents']:
                objects.append(item['Key'])
            if file in objects:
                response = s3.delete_object(Bucket=bucket1, Key=file)
                res='deleted'
            else:
                res='no such file'
    except Exception as e:
        res=type(e).__name__
    return render(request,'Delete_file.html',{'result':res})

def copy_file(request):
    result='not moved'
    bucket1=request.POST['from_bucket']
    bucket2=request.POST['to_bucket']
    file=request.POST['file_name']
    try:
        if request.POST:
            s3= boto3.client('s3',
            aws_access_key_id=os.getenv('ACCESSKEY'),
            aws_secret_access_key=os.getenv('SECRETKEY')
            )
            copy_source = {
                'Bucket': bucket1,
                'Key': file
            }
            s3.copy_object(CopySource=copy_source, Bucket=bucket2, Key=file)
            result='moved'
    except Exception as e:
        result=type(e).__name__
    return render(request,'copy_file.html',{"result":result})

def move_file(request):
    result='not moved'
    try:
        if request.POST:
            bucket1=request.POST['from_bucket']
            bucket2=request.POST['to_bucket']
            file=request.POST['file_name']
            s3= boto3.client('s3',
            aws_access_key_id=os.getenv('ACCESSKEY'),
            aws_secret_access_key=os.getenv('SECRETKEY')
            )
            copy_source = {
                'Bucket': bucket1,
                'Key': file
            }
            s3.copy_object(CopySource=copy_source, Bucket=bucket2, Key=file)

            s3.delete_object(Bucket=bucket1, Key=file)

            result='moved'
    except Exception as e:
        result=type(e).__name__
    return render(request,'move_file.html',{'result':result})
    