console.log('Bot Handler Started.');

const AWS = require('aws-sdk');
const docClient = new AWS.DynamoDB.DocumentClient({region: 'us-west-1'});

exports.handler = function(e, ctx, callback) {
    let botId = +e?.botid ?? -1;
    
    const findBot = {
        TableName : 'Sensible-App-Bot-Data',
        Key: {
          botid: botId
        }
    }; 
    
    const params = {
        Item: {
            botid: botId,
            data: [0,0,0,0,0,0],
            energy: 0,
        },
        TableName: "Sensible-App-Bot-Data"
    };

    docClient.get(findBot, function(err, data){
        if(err){
            callback(err, null);
        }else{
            docClient.put(params, function(err, data){
                if(err){
                    callback(err, null);
                }else{
                    callback(null, data);
                }
            });
        }
    });
};
