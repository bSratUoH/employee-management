from utils.connection import getClient, getResource
from utils.resources import employee_table
from boto3.dynamodb.conditions import Key

ddbClient = getClient("dynamodb")
ddbResource = getResource("dynamodb")

class DDBHelper:
    def __init__(self, ddbClient=ddbClient, ddbResource=ddbResource):
        self.ddbClient = ddbClient
        self.ddbResource = ddbResource

    def getDDBTableObject(self, table):
        return self.ddbResource.Table(table)
    
    def queryDDB(self, regId, table=employee_table):
        empTable = self.getDDBTableObject(table)
        resp = empTable.query(
                KeyConditionExpression=Key('regid').eq(regId)
            )
        return resp

    def putItem(self, data, table=employee_table):
        empTable = self.getDDBTableObject(table)
        resp = empTable.put_item(Item=data)
        return resp


    def getItem(self, table=employee_table, pk=None, sk=None):
        empTable = self.getDDBTableObject(table)
        if pk and sk:
            key = {"email": sk, "regId": pk}
        elif sk:
            key = {"email": sk}
        else:
            key = {"regId": pk}

        resp = empTable.get_item(Key=key)
        return resp

    def deleteItem(self, regId, table=employee_table):
        empTable = self.getDDBTableObject(table)
        resp = empTable.delete_item(Key={'regId': regId})
        return resp

    def updateItem(self, items, table=employee_table):
        empTable = self.getDDBTableObject(table)
        regId = items["regId"]
        del items["regId"]
        resp = empTable.update_item(
            Key={'regId': regId},
            AttributeUpdates=items
        )
        return resp
        