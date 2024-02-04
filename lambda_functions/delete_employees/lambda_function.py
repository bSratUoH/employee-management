import simplejson as json
from utilities.ddbHelper import DDBHelper
from utilities.utils import lambdaExceptionWrapper

ddbHelperObj = DDBHelper()


@lambdaExceptionWrapper()
def lambda_handler(event, context):
        
    # Extract regid from the request body
    request_body = json.loads(event['body'])
    regId = request_body.get('regId', None)

    # Check if employee with regid exists
    resp = ddbHelperObj.getItem(regId)
    if not resp.get("Item"):
        return {
            'statusCode': 200,
            'body': json.dumps({"message": f"No employee found with regid {regId}", "success": False})
        }

    # Delete the employee
    resp = ddbHelperObj.deleteItem(regId)

    return {
        'statusCode': 200,
        'body': json.dumps({"message": "Employee deleted successfully", "success": True})
    }
