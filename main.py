from flask import Flask
from flask import render_template, flash, redirect, url_for,request
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
import logging
import boto3
from botocore.exceptions import ClientError
#import key_config as keys


# files create in local server

s3 = boto3.client('s3',
                    aws_access_key_id="something",
                    aws_secret_access_key= "something",
                     )

BUCKET_NAME='Bucket_NAME'

def create_bucket(bucket_name, region=None):
    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# to upload file


app = Flask(__name__)
api = Api(app)

class upload(Resource):
    def post(self):
         if request.method == 'POST':
             img = request.files['file']
             if img:
                filename = secure_filename(img.filename)
                img.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
                )
                msg = "Upload Done ! "

         return redirect(url_for("index",msg =msg))
class create(Resource):
    def post(self):
        if request.method =="POST":
            bucket_name = request.form.get("bname")
            region = "us-east-2"
            try:
                if region is None:
                    s3_client = boto3.client('s3')
                    s3_client.create_bucket(Bucket=bucket_name)
                else:
                    s3_client = boto3.client('s3', region_name=region)
                    location = {'LocationConstraint': region}
                    s3_client.create_bucket(Bucket=bucket_name,
                                            CreateBucketConfiguration=location)
            except ClientError as e:
                logging.error(e)
        msg="CREATED!!"
        return redirect(url_for("index",msg =msg))

        
api.add_resource(upload, "/upload")
api.add_resource(create, "/create")

@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    return render_template('index.html')    


if __name__ == "__main__":
    app.run(debug=True)
