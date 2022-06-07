console.log('Bot Handler Started.');

const AWS = require('aws-sdk');
const docClient = new AWS.DynamoDB.DocumentClient({region: 'us-west-1'});

exports.handler = function(e, ctx, callback) {
    let allItems = {
        TableName: 'Sensible-App-Bot-Data',
        Limit: 50
    };
    
  
    docClient.scan(allItems, function(err, data){
        if(err){
            callback(err, null);
        }else{
            let botId = 0;
            let params = {};
            for (let i = 0; i < data.Items.length; i++) {
                botId = data.Items[i].botid;
                params = {
                    Item: {
                        botid: botId,
                        data: [0,0,0,0,0,0],
                        energy: 0
                    },
                    TableName: "Sensible-App-Bot-Data"
                };
            
                docClient.put(params, function(err, data){
                    if(err){
                        callback(err, null);
                    }else{
                        callback(null, data);
                    }
                });
            }
        }
    })};
