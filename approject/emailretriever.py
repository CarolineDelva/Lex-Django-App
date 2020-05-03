import win32com.client
import os 
import re
import boto3
from botocore.exceptions import NoCredentialsError
from csci-utils.io import atomic_write


from dotenv import load_dotenv

load_dotenv(dotenv_path ='.env')
"""
loading the env file to access the environment variables
"""


my_outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

folder = my_outlook.GetDefaultFolder(6).Folders.Item("Lexology")
filename = "Urls.parquet"
directory = "data/"
for item in folder.Items:
    
    emailbody = item.body
  
    urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', emailbody)
    



with atomic_write(filename, as_file=False) as f:
  

    if not os.path.exists(directory):
        os.mkdir(directory)

    f = os.path.join(directory, filename)  

    urls.to_parquet(f)



ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
SECRET_KEY = os.environ['AWS_SECRET_ACCESS_KEY']


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


uploaded = upload_to_aws('local_file', 'bucket_name', 's3_file_name')
    
