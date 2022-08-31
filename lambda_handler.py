def handle(context, event):

    print("Handling From")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "message": "Complete"
        }
    }