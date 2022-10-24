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
    
    image_numb = random.randint(1, 731)
    
    if random.randint(1, 2) == 2 & image_numb > 602:
        name_image = "%s%s" % (image_numb, ".mp4")
        name_temp = "/tmp/%s" % (name_image)
        
    else:
        name_image = "%s%s" % (image_numb, ".jpg")
        name_temp = "/tmp/%s" % (name_image)
    
    
    s3_resource = boto3.resource('s3', 
        aws_access_key_id=aws_access_key_id, 
        aws_secret_access_key=aws_secret_access_key)
        

    s3_resource.Bucket('nayeonbucket').download_file(name_image, name_temp)
    
    status = '#나연 #NAYEON #TWICE'
    
    
    #Authenticating
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret_token)
    
    #Create API object
    api = tweepy.API(auth)
    
    #Create a tweet
    api.update_with_media(name_temp, status)
