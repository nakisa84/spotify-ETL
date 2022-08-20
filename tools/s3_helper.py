from datetime import datetime
from operator import imod

import uuid
from warnings import catch_warnings
import boto3




class s3:
    def __init__(self):
        self.session = boto3.session.Session()
        self.resource = boto3.resource('s3')
        self.client = self.resource.meta.client


    def create_bucket_name(self,bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
        if bucket_prefix:
            name = ''.join([bucket_prefix, str(uuid.uuid4())]) 
            return name
        return str(uuid.uuid4()) 


    def create_bucket(self,bucket_prefix = None,bucket_name = None):
        if bucket_name is None:
            bucket_name = self.create_bucket_name(bucket_prefix)
        # try:   
        if self.is_bucket_exists(bucket_name):
             print(f"{bucket_name}-already exists.") 
             return
        bucket_response = self.client.create_bucket(Bucket=bucket_name)
        print(f"{bucket_response['Location']} has been created.")
        return bucket_name, bucket_response 
        # except:
        #     print("An exception occurred")
        

    def save_data_s3(self,playlist,bucket):
        date = datetime.now()
        filename = f'{date.year}/{date.month}/{date.day}/{playlist}.csv'
        self.client.upload_file(Filename = f'/tmp/{playlist}.csv',
                            Bucket = bucket,
                            Key = filename)

    def read_data_s3(self,bucket,key,filename):
        keys = key.split('/')
        self.client.download_file(Bucket = bucket,
                                Key = f'{key}/{filename}', 
                                Filename = f"data/{keys[0]}_{keys[1]}_{keys[2]}_{filename}")

    def get_buckets_s3(self):
        response = self.client.list_buckets()
        if not response['Buckets']:
             print("No buckets found!")
             return None 
        print("Listing Amazon S3 Buckets:")
        for bucket in response['Buckets']:
            print(f"-- {bucket['Name']}")
        return response['Buckets'] 
     


    def delete_buckets_s3(self):
        buckets = self.get_buckets_s3()
        if not buckets:
            return
        for item in buckets:
            print(f"\n---deleting buckets---> {item['Name']}")
            answer = input('\nconfirm to delete? ')
            if answer.lower() == 'y':
                bucket = self.resource.Bucket(item['Name'])
                bucket.objects.all().delete()
                self.client.delete_bucket(Bucket=item['Name'])
                print(f"Amazon S3 {item['Name']} has been deleted") 
            continue    

    def is_bucket_exists(self,bucket_name):
         buckets = self.get_buckets_s3()
         if not buckets:
            return False
         for item in buckets:
            if item['Name'] == bucket_name:
                return True
         return False     


