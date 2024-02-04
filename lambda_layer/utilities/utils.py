from uuid import uuid4
from .logger import logger
import json

def getEmployeeId():
    # Generate a unique employee ID using UUID4
    return format(str(uuid4()))



def exception_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return response
        except BaseException as baseExe:
            logger.error(f"error while executing function- {func.__name__}\n\n", exc_info=True)
            raise Exception(str(baseExe))

    return wrapper

def lambdaExceptionWrapper(caller=None):
    """
    A decorator that wraps the passed in function and logs exceptions
    """

    from functools import wraps

    def decorator(func):
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = {}
            try:
                response = func(*args, **kwargs)
            except Exception as e:
                err = f"Logger caught an exception in {caller or func.__name__}: {e}"
                logger.exception(err)
                response = {
                    'statusCode': 500,
                    'body': json.dumps({
                        'message': 'Something went wrong',
                        'success': False
                    })
                }
            return response

        return wrapper

    return decorator
