import json
import boto3
import os



def lambda_handler(event, context):
    
    prod_account=os.environ["PROD_ACCOUNT"]
    dev_account=os.environ["DEV_ACCOUNT"]

    list_buckets_cross_acct(dev_account)
    list_buckets_cross_acct(prod_account)

    return {
        "statusCode": 200,
        "body": "Success"
    }


def list_buckets_cross_acct(acct_number):
    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn=f"arn:aws:iam::{acct_number}:role/aws-controltower-ReadOnlyExecutionRole",
        RoleSessionName="cross_acct_lambda"
    )
    
    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']

    # create service client using the assumed role credentials, e.g. S3
    client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )

    response = client.list_buckets()

    print(response)