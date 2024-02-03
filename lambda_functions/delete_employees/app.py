import json
from utils.ddbHelper import DDBHelper

ddbHelperObj = DDBHelper()


def lambda_handler(event, context):
    """Sample pure Lambda function"""
    try:
        
        # Extract regid from the request body
        request_body = json.loads(event['body'])
        regId = request_body.get('regid', None)
        
        # if not regid:
        #     return {
        #         'statusCode': 400,
        #         'body': json.dumps({"message": "Missing 'regid' in the request body", "success": False})
        #     }

        # Check if employee with regid exists
        resp = ddbHelperObj.getItem(pk=regId)
        if 'Item' not in resp:
            return {
                'statusCode': 200,
                'body': json.dumps({"message": f"No employee found with regid {regid}", "success": False})
            }

        # Delete the employee
        resp = DDBHelper.deleteItem(regId)

        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Employee deleted successfully", "success": True})
        }
    
    except Exception as e:
        return {
            'statusCode': 200,
            'body': json.dumps({"message": f"Employee deletion failed: {str(e)}", "success": False})
        }