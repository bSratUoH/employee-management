from uuid import uuid4

def getEmployeeId():
    # Generate a unique employee ID using UUID4
    return format(str(uuid4()))

