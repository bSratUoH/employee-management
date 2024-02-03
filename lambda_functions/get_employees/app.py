import json
from utils.connection import table
from utils.ddbHelper import DDBHelper

ddbHelperObj = DDBHelper()


def lambda_handler(event, context):
    """Sample pure Lambda function"""
    try:
        # Extract regid from the query parameters
        queryParams = event.get('queryStringParameters', {})
        regId = queryParams["regid"] if queryParams else None

        if regId:
            # Retrieve a single employee by regid
            resp = ddbHelperObj.queryDDB(regId)

            if resp.get('Items'):
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        "message": "Employee details found",
                        "success": True,
                        "employees": resp['Items']
                    })
                }
        else:
            # Retrieve all employees
            response = table.scan()

            if response.get('Items'):
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        "message": "Employee details found",
                        "success": True,
                        "employees": response['Items']
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
    except Exception as e:
        return {
            'statusCode': 200,
            'body': json.dumps({
                "message": f"Error: {str(e)}",
                "success": False,
                "employees": []
            })
        }
    
    