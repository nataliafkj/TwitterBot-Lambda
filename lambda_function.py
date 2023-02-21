import os
import tweepy
import requests
from io import BytesIO
import boto3
import random


def lambda_handler(event, context):
    api_key = os.environ['api_key']
    api_secret = os.environ['api_secret']
    bearer_token = os.environ['bearer_token']
    access_token = os.environ['access_token']
    access_secret_token = os.environ['access_secret_token']
    aws_access_key_id = os.environ['aws_access_key_id']
    aws_secret_access_key = os.environ['aws_secret_access_key']
    
    bucket_name = "nayeonbucket"
    
    s3_resource = boto3.resource('s3', 
        aws_access_key_id=aws_access_key_id, 
        aws_secret_access_key=aws_secret_access_key)
    
    #Create image list
    my_bucket = s3_resource.Bucket('nayeonbucket')
    a = [my_bucket_object.key for my_bucket_object in my_bucket.objects.all()] 
    
    #Choose a photo
    image_numb = random.randint(0, len(a))
    
    photo_name = a[image_numb]
    
    name_temp = "/tmp/%s" % (photo_name)
    
    status = '#나연 #NAYEON #TWICE'
    
    s3_resource.Bucket('nayeonbucket').download_file(photo_name, name_temp)
    
    #Authenticating
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret_token)
    
    #Create API object
    api = tweepy.API(auth)
    
    #Create a tweet
    api.update_with_media(name_temp, status)
    
    #Delete image posted
    s3 = boto3.client('s3', 
        aws_access_key_id = aws_access_key_id, 
        aws_secret_access_key = aws_secret_access_key)
    s3.delete_object(Bucket='nayeonbucket', Key=photo_name)
