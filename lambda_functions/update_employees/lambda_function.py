import simplejson as json
from utilities.ddbHelper import DDBHelper
from utilities.utils import lambdaExceptionWrapper

ddbHelperObj = DDBHelper()

@lambdaExceptionWrapper()
def lambda_handler(event, context):
        
    # taking requested data in request body
    request_body = json.loads(event['body'])
    
    # Check if employee with regid exists
    regId = request_body['regId']
    resp = ddbHelperObj.getItem(regId)

    if not resp.get("Item"):
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'No employee found with the given details',
                'success': False
            })
        }
    
    else:
        ddbHelperObj.updateItem(request_body)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Employee detail updated',
                'success': False
            })
        }
