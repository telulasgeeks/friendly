from app import server as app

def handler(event, context):
    return app(event, context)