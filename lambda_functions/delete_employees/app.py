import json
from utils.clients import table


def lambda_handler(event, context):
    """Sample pure Lambda function"""
    try:
        
        # Extract regid from the request body
        request_body = json.loads(event['body'])
        regid = request_body.get('regid', None)
        
        if not regid:
            return {
                'statusCode': 400,
                'body': json.dumps({"message": "Missing 'regid' in the request body", "success": False})
            }

        # Check if employee with regid exists
        response = table.get_item(Key={'regid': regid})
        if 'Item' not in response:
            return {
                'statusCode': 200,
                'body': json.dumps({"message": f"No employee found with regid {regid}", "success": False})
            }

        # Delete the employee
        table.delete_item(Key={'regid': regid})

        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Employee deleted successfully", "success": True})
        }
    except Exception as e:
        return {
            'statusCode': 200,
            'body': json.dumps({"message": f"Employee deletion failed: {str(e)}", "success": False})
        }