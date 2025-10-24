from settings.logging import auto_logger, setup_logger
import json
from fastapi import FastAPI
from fastapi.routing import APIRoute

app = FastAPI()
logger = setup_logger(__name__)
auto_logger(logger)


testobj = json.loads("{\"test\": \"testobj\"}")
logger.log(4, 'test', testobj)
loggerobj = logger.LogRecord(
    "testRecord", 3, __file__, 11, 'test message', None, None, None, None)

print('\n'.join(sorted(loggerobj.__dict__.keys())))


def home():
    ''''''


def contact():
    ''''''


def history():
    ''''''


def shortener():
    ''''''


def main():

    routes = [APIRoute("/", home, description='landing page', responses={
        200: {"description": "Successful Response"},
        500: {"description": "Internal Server Error"},
    }, methods=['GET']),
        APIRoute("/contact", contact, description='contact page', responses={
            200: {"description": "Successful Response"},
            500: {"description": "Internal Server Error"},
        }, methods=['GET']),
        APIRoute("/history", history, description='history of requests', responses={
            200: {"description": "Successful Response"},
            500: {"description": "Internal Server Error"},
        }, methods=['GET']),
        APIRoute("/shortener", shortener, description='shortener page', responses={
            200: {"description": "Successful Response"},
            500: {"description": "Internal Server Error"},
        }, methods=['GET'])]

    logger.log(4, 'test', testobj)
    logger.info('hoo')


if __name__ == '__main__':
    main()
