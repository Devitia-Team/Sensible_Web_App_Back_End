import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    botid = event["queryStringParameters"]["botid"]
    
    client.update_item(
        TableName='egr102-bot-kill-id',
        Key={'id': {'N': '1'}},
        AttributeUpdates={
            'botid': {
                'Value': {'N': botid },
                'Action': 'PUT'
            }
        }
    )
    
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        'body': '',
    }
