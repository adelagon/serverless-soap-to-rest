import os
import uuid
import json
from zeep import Client

client = Client(
    wsdl="{}/?wsdl".format(os.environ['SOAP_ENDPOINT']))

def handler(event, context):
    input = json.loads(event['body'])
    insurance_cost = client.service.submit_car_application(
        first_name=input['first_name'],
        last_name=input['last_name'],
        make=input['make'],
        model=input['model'],
        year=input['year'],
        current_price=input['current_price']
    )
    
    message = {
        "status": "approved",
        "insurance_cost": insurance_cost,
        "application_id": str(uuid.uuid4()),
        "input": input     
    }

    return {
        "statusCode": 200,
        "body": json.dumps(message),
        "headers": {'Content-Type': 'application/json'}
    } 
