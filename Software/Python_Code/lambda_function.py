import json
import boto3

def lambda_handler(event, context):
    # Create a DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    
    # Specify the table name
    table_name = 'Plant_Data'
    
    # Get the DynamoDB table
    table = dynamodb.Table(table_name)
    
    # Extract values from the incoming event
    timestamp = event.get('timestamp', '')
    fluid_temperature = event.get('fluid_temperature', '')
    heater_status = event.get('heater_status', '')
    pump1_status = event.get('pump1_status', '') 
    pump2_status = event.get('pump2_status', '')
    level_tank1 = event.get('level_tank1', '')
    level_tank2 = event.get('level_tank2', '')
    valve1_status = event.get('valve1_status', '')
    valve2_status = event.get('valve2_status', '')

    # Put item into DynamoDB table
    response = table.put_item(
        Item={
        'timestamp' : timestamp,
        'fluid_temperature': fluid_temperature,
        'heater_status': heater_status,
        'pump1_status': pump1_status,
        'pump2_status': pump2_status,
        'level_tank1': level_tank1,
        'level_tank2': level_tank2,
        'valve1_status': valve1_status,
        'valve2_status': valve2_status
        }
        
    )
    
        # Check if fluid_temperature is greater than 25
    if fluid_temperature is not None and fluid_temperature > 25:
        # If temperature is greater than 25, trigger SNS
        sns_client = boto3.client('sns')

        sns_topic_arn = 'arn:aws:sns:us-west-2:715578268860:IIoT'

        # Message to be sent to SNS
        message = f"Alert: Fluid temperature is greater than 30. Current temperature: {fluid_temperature}"

        # Publish the message to the SNS topic
        sns_client.publish(TopicArn=sns_topic_arn, Message=message, Subject="High Fluid Temperature Alert")

        # Return a success response
        return {
            'statusCode': 200,
            'body': json.dumps('SNS notification sent successfully')
        }
    else:
        # If temperature is not greater than 25, return a response
        return {
            'statusCode': 200,
            'body': json.dumps('Fluid temperature is not greater than 25. No SNS notification sent.')
        }

    # Return response (you might want to customize this based on your use case)
    return {
        'statusCode': 200,
        'body': f'Successfully stored data in DynamoDB: {response}'
    }
    