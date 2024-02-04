import simplejson as json
from utilities.ddbHelper import DDBHelper
from utilities.utils import lambdaExceptionWrapper

ddbHelperObj = DDBHelper()


@lambdaExceptionWrapper()
def lambda_handler(event, context):
        
    # Extract regid from the query parameters
    queryParams = event.get('queryStringParameters', {})
    print(queryParams)
    regId = queryParams["regId"] if queryParams else None

    if regId:
        # Retrieve a single employee by regid
        resp = ddbHelperObj.getItem(regId)

        if resp.get('Item'):
            return {
                'statusCode': 200,
                'body': json.dumps({
                    "message": "Employee details found",
                    "success": True,
                    "employees": resp['Item']
                })
            }
    else:
        # Retrieve all employees
        resp = ddbHelperObj.scanDDBTable()

        if resp.get('Items'):
            return {
                'statusCode': 200,
                'body': json.dumps({
                    "message": "Employee details found",
                    "success": True,
                    "employees": resp['Items']
                })
            }
        
    return {
                'statusCode': 200,
                'body': json.dumps({
                    "message": "Employee details not found",
                    "success": False,
                    "employees": []
                })
            }
