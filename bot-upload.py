import json
import boto3
from decimal import Decimal

resource = boto3.resource('dynamodb')
data_table = resource.Table('Sensible-App-Bot-Data')
kill_table = resource.Table('egr102-bot-kill-id')

def lambda_handler(event, context):
    data = eval(event['data'])

    botid = data[0]
    search = data_table.get_item(
        Key={'botid': botid}
    )
    
    if 'Item' in search:
        energy = search['Item']['energy']
    else:
        energy = Decimal(0.0)
    energy += Decimal(abs(data[-1]))
    
    data_table.update_item(
        Key={'botid': botid},
        AttributeUpdates={
            'data': {
                'Value': [Decimal(n) for n in data[1:-1]],
                'Action': 'PUT'
            },
            'energy': {
                'Value': energy,
                'Action': 'PUT'
            }
        }
    )
    
    kill_id = kill_table.get_item(
        Key={'id': 1}
    )['Item']['botid']
    
    doKill = botid == int(kill_id)
    
    if doKill:
        kill_table.update_item(
            Key={'id': 1},
            AttributeUpdates={
                'botid': {
                    'Value': -1,
                    'Action': 'PUT'
                }
            }
        )
    
    return {
        'statusCode': 200,
        'isBase64Encoded': False,
        'headers': {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
          'endLoop': doKill,
        }),
    }
