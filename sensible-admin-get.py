import json
import boto3

# used to access DynamoDB
client = boto3.client('dynamodb')

# this function is called when the client makes a request
# to the API gateway.
def lambda_handler(event, context):
    # get all rows from DynamoDB
    data = client.scan(TableName='Sensible-App-Bot-Data')
    
    if 'Items' not in data:
        json_status_code = 404
        response = {
            'statusCode': json_status_code,
        },
    else:
        # "By default DynamoDB returns us a Dictionary of lists of dictionaries
        # which to be honest is very gross. The below code extracts the data
        # and beautifies it." - Jake Speyer, 2022
        bot_data = []
        for bot in data['Items']:
            bot_data.append({
                'botId': bot['botid']['N'],
                'distanceA': round(float(bot['data']['L'][0]['N']),2),
                'distanceB': round(float(bot['data']['L'][1]['N']),2),
                'voltageA': bot['data']['L'][2]['N'],
                'voltageB': bot['data']['L'][3]['N'],
                'lightA': bot['data']['L'][4]['N'],
                'lightB': bot['data']['L'][5]['N'],
                'energy': bot['energy']['N']
            })
    
        json_status_code = 200
  
        response = {
            'statusCode': json_status_code,
            'data': bot_data,
            'headers': {
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': '*'
            },
        }
    return response
