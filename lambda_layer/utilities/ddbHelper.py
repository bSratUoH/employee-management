from .connection import getClient, getResource
from .resources import employeeTable, empGlobalIndex
from .utils import exception_wrapper

ddbClient = getClient("dynamodb")
ddbResource = getResource("dynamodb")

class DDBHelper:
    def __init__(self, ddbClient=ddbClient, ddbResource=ddbResource):
        self.ddbClient = ddbClient
        self.ddbResource = ddbResource

    @exception_wrapper
    def getDDBTableObject(self, table):
        return self.ddbResource.Table(table)
    
    @exception_wrapper
    def queryDDB(self, attr, table=employeeTable):
        empTable = self.getDDBTableObject(table)
        resp = empTable.query(
            IndexName=empGlobalIndex,
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={
                ':email': attr
            }
        )
        return resp

    @exception_wrapper
    def putItem(self, data, table=employeeTable):
        empTable = self.getDDBTableObject(table)
        resp = empTable.put_item(Item=data)
        return resp

    @exception_wrapper
    def getItem(self, pk, table=employeeTable):
        empTable = self.getDDBTableObject(table)
        resp = empTable.get_item(Key={"regId": pk})
        return resp

    @exception_wrapper
    def deleteItem(self, regId, table=employeeTable):
        empTable = self.getDDBTableObject(table)
        resp = empTable.delete_item(Key={'regId': regId})
        return resp

    @exception_wrapper
    def updateItem(self, items, table=employeeTable):
        empTable = self.getDDBTableObject(table)
        regId = items["regId"]
        del items["regId"]

        updateParams = self.build_update_params(items, items.keys())
        print(updateParams)
        resp = empTable.update_item(
            Key={'regId': regId},
            UpdateExpression=updateParams["UpdateExpression"],
            ExpressionAttributeNames=updateParams["ExpressionAttributeNames"],
            ExpressionAttributeValues=updateParams["ExpressionAttributeValues"],
            ConditionExpression="attribute_exists(regId)",
            ReturnValues="ALL_NEW",
        )
        return resp

    @exception_wrapper  
    def scanDDBTable(self, table=employeeTable):
        empTable = self.getDDBTableObject(table)
        resp = empTable.scan()
        return resp
    
    def build_update_params(self, data, attributes):
        """
        arranging all the parameters for updating a record
        :param data: dict
        :return: tuple
        """
        updateExpression = "set "
        expressionAttributeNames = {}
        expressionAttributeValues = {}
        for index, attributeName in enumerate(attributes):
            attribKey = f"#attr{index}"
            valueKey = f":val{index}"
            expressionToAdd = f"{attribKey} = {valueKey}"
            if index == 0:
                updateExpression += expressionToAdd
            else:
                updateExpression += f",{expressionToAdd}"
            expressionAttributeNames[attribKey] = attributeName
            expressionAttributeValues[valueKey] = data[attributeName]

        return {
            "UpdateExpression": updateExpression,
            "ExpressionAttributeNames": expressionAttributeNames,
            "ExpressionAttributeValues": expressionAttributeValues,
        }

    