import boto3


def getClient(resource):
    return boto3.client(resource)


def getResource(resource):
    return boto3.resource(resource)
