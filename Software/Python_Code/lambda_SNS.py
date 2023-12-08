import json
import boto3

def lambda_handler(event, context):
    # Parse the incoming JSON data
    plant_data = json.loads(event['body'])

    # Extract fluid_temperature from the JSON data
    fluid_temperature = plant_data.get('fluid_temperature')

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
