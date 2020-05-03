import os

from luigi import ExternalTask, Parameter, Task, LocalTarget
from csci_utils.luigi.target import SuffixPreservingLocalTarget
from luigi.contrib.s3 import S3Target

import luigi
import boto3
import botocore
import torch
from PIL import Image
import io
from luigi import format



class ContentImage(ExternalTask):
    IMAGE_ROOT = "s3://advancedpythonproject/"

    
    # Root S3 path, as a constant

    # Name of the image
    image = Parameter(default="LuigiMarioParty.jpg") # Filename of the image under the root s3 path

    def output(self):
        # return the S3Target of the image
        return S3Target(path=self.IMAGE_ROOT + self.image, format=luigi.format.Nop)
#
class SavedModel(ExternalTask):
    MODEL_ROOT = "s3://advancedpythonproject/"

    model = Parameter(default="rain_princess.pth") # Filename of the model

    def output(self):
        # return the S3Target of the model
         return S3Target(path=self.MODEL_ROOT + self.model, format=luigi.format.Nop)

class DownloadModel(Task):
    S3_ROOT = "s3://carolinedelvapset4bucket/"
    LOCAL_ROOT = os.path.abspath('data')
    SHARED_RELATIVE_PATH = 'saved_models'

    model = Parameter(default="rain_princess.pth")# luigi parameter

    def requires(self):
        # Depends on the SavedModel ExternalTask being complete
        # i.e. the file must exist on S3 in order to copy it locally

        return SavedModel(model=self.model)
        

    def output(self):
        return SuffixPreservingLocalTarget(os.path.join(self.LOCAL_ROOT,
                                        self.SHARED_RELATIVE_PATH,
                                        self.model))

    def run(self):
       
        import io, torch, json
        with self.input().open("r") as input_file: 
            model = io.BytesIO(input_file.read())
        model = torch.load(model)
        self.output().open('w').close()
        torch.save(model, self.output().path)



class DownloadImage(Task):
    S3_ROOT = "s3://carolinedelvapset4bucket/"
    LOCAL_ROOT = os.path.abspath('data')
    SHARED_RELATIVE_PATH = 'images'

    image = Parameter()# Luigi parameter

    def requires(self):
        # Depends on the SavedModel ExternalTask being complete
        # i.e. the file must exist on S3 in order to copy it locally
        return ContentImage(image=self.image)
        

    def output(self):
        return SuffixPreservingLocalTarget(os.path.join(self.LOCAL_ROOT,
                                        self.SHARED_RELATIVE_PATH,
                                        self.image))

    def run(self):

        with self.input().open("r") as input_file:
            from PIL import Image 
            image_load = Image.open(input_file)
            self.output().open('w').close()
            image_load.save(self.output().path)


            