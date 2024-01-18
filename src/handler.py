from CSVChat import CSVChat

import json

def handler(event: dict, context: dict) -> dict:
    body = json.loads(event['body'])
    question = body['question']

    try:
        chat = CSVChat()
        answer = chat(question)
    
        return {
            'statusCode': 200,
            'body': answer
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }