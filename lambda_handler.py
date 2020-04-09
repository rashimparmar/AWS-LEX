import json
import csv
import boto3
import json
import dateutil.parser
import datetime
import time
import os
import math
import random
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    return response

""" --- Function that return employee name --- """

def main_calc_employee_dept(Department_id):
    s3=boto3.client("s3")
    filename='employeeDetails.csv'
    fileObj = s3.get_object(Bucket = "demo-awslex", Key=filename)
    rows = fileObj['Body'].read().decode('utf-8').split('\r\n')
        
    reader = csv.reader(rows)
    rows = []
    header = next(reader)
    for i in reader:
        rows.append(i)
        
    #Employee name search based on department_id
    x=0 #row iterator
    output=[]
    
    for i in rows:
        if rows[x][0] == Department_id: 
            output.append(rows[x][2])
        x=x+1
    if not output :
        return ("There are no Employees in this department")
    else:
        return ('Employees names are {}'.format(output))
        
def return_EmployeeName(intent_request):
    """
    Performs dialog management and fulfillment for returning employee's department Name.
    """
    Department_id = intent_request['currentIntent']['slots']['DepartmentID']
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    
    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        slots = intent_request['currentIntent']['slots']
    return close(
        output_session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Hello! {}'.format(main_calc_employee_dept(Department_id))
        }
    )

""" --- Intents --- """
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """
    logger.debug('dispatch intentName={}'.format(intent_request['currentIntent']['name']))
    intent_name='ReturnEmployeeName'
    
    # Dispatch to your bot's intent handlers
    if intent_name == 'ReturnEmployeeName':
        return return_EmployeeName(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')

""" --- Main handler --- """
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return dispatch(event)