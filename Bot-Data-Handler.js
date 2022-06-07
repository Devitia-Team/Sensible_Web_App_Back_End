console.log('Bot Handler Started.');

const AWS = require('aws-sdk');
const docClient = new AWS.DynamoDB.DocumentClient({region: 'us-west-1'});

/*global sensors*/
/*global newEnergy*/
/*global clearFlag*/

exports.handler = function(e, ctx, callback) {
    let sensors
    let newEnergy
    let clearFlag
    
    // Sets a constant with the value of the event body.
    // (It is a weirdly formatted JSON.)
    // EX: "data: [1,2,3,4,5,6,7]"
    const botData = e.body ? JSON.parse(e.body) : e;
    // grabs just the numeric values of the bot data ([1,2,3,4,5,6,7])
    let dataList = botData.data;
    let bot = dataList[0];
    
    if(dataList.length <= 7){// ID, DIS_SENSOR, DIS_SENSOR, VOL_SENSOR, VOL_SENSOR, LIG_SENSOR, LIG_SENSOR
        sensors = dataList.slice(1);
        newEnergy = 0;
        clearFlag = 0;
    }else{// ID, DIS_SENSOR, DIS_SENSOR, VOL_SENSOR, VOL_SENSOR, LIG_SENSOR, LIG_SENSOR, ENERGY, CLEARFLAG
        sensors = dataList.slice(1, 7);
        newEnergy = dataList[7];
        clearFlag = dataList[8];
    }
    

    
    if(clearFlag == 1){
      let params = {
          Item: {
              botid: bot,
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
      })
    }else{
      const findBot = {
        TableName : 'Sensible-App-Bot-Data',
        Key: {
          botid: bot
        }
      }
    
      docClient.get(findBot, function(err, data){
        if(err){
            callback(err, null);
        }else{
            let oldEnergy = data['Item']['energy']
            
                let finalEnergy = oldEnergy + newEnergy;
    
                let params = {
                    Item: {
                        botid: bot,
                        data: sensors,
                        energy: finalEnergy
                    },
                    TableName: "Sensible-App-Bot-Data"
                };
                
                docClient.put(params, function(err, data){
                    if(err){
                        callback(err, null);
                    }else{
                        callback(null, data);
                    }
                })
        }
      })
    }
};
