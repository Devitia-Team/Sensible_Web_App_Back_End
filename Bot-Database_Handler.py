import json
import boto3

#Sets active service to DynamoDB
client = boto3.resource('dynamodb')
table = client.Table('Sensible-App-Bot-Data')

#Lambda handler that takes care of connecting to
#the DynamoDB Table.
#
#Checks to see if the bot exists in the table. If it
#does exist it will return a Json packet with the
#sensor data. If it does not contain the bot id
#then it will throw a status code of 404 indicating to
#the client that the bot does not exist.
def lambda_handler(event, context):
  bot_id = int(event['botId'])
  data = table.get_item(
    #botid refers to the primary key in the DynamoDB Database
    #N refers to the key type (numeric)
    Key={
        'botid': bot_id
    }
  )
  if 'Item' not in data:
    json_status_code = 404
    response = {
      'statusCode': json_status_code,
    },
  else:
    #By default DynamoDB returns us a Dictionary of lists of dictionaries
    #which to be honest is very gross. The below code extracts the data
    #and beautifies it.
    json_item = data['Item']
    json_bot_data = {
      'distanceA': round(float(json_item['data'][0]),2),
      'distanceB': round(float(json_item['data'][1]),2),
      'voltageA': json_item['data'][2],
      'voltageB': json_item['data'][3],
      'lightA': json_item['data'][4],
      'lightB': json_item['data'][5],
      'energy': json_item['energy'],
    }
    
    json_status_code = 200
  
    response = {
        'statusCode': json_status_code,
        'data': json_bot_data,
        'headers': {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
    }
  return response
