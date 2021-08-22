"""Serverless Slack Bot Lambda handler."""

import json
import os

import urllib
import urllib.parse
import urllib.request

from lib.log import Log


BOT_TOKEN = os.getenv("BOT_TOKEN")

SLACK_URL = "https://slack.com/api/chat.postMessage"


def verify_request(event, logger):
    """
    Refer to this document for information on verifying slack requests:
    https://api.slack.com/docs/verifying-requests-from-slack
    """
    try:
        return event['body']['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    except Exception as err:
        logger.error(f">> Something happen during while checking verification token: {err}")
        return None


def bot(event, _context):
    logger = Log.logger(desc="Aws serverless slack bot handler")
    logger.info("Request Event: {}".format(event))

    if not verify_request(event, logger=logger):
        logger.error(f"The request is not authorized to perform NotifyBot call.")
        return {'statusCode': 401}

    try:
        response = {}
        if 'body' in event:
            request_body_json = event['body']
            logger.info('Received API Gateway Request with Body: {}'.format(request_body_json))

            if 'challenge' in request_body_json:
                challenge = request_body_json["challenge"]
                logger.info('Challenge: {}'.format(challenge))
                challenge_response = {'challenge': challenge}
                response = {
                    'status_code': 200,
                    'body': json.dumps(challenge_response)
                }

            if 'event' in request_body_json:
                slack_event = request_body_json['event']
                logger.info('Received Slack Event with Body: {}'.format(slack_event))
                if 'bot_id' in slack_event:
                    logger.warn('Ignored bot event')
                else:
                    user_message = slack_event['text']
                    logger.info('User Message: {}'.format(user_message))

                    bot_reply = "Hello I'm NotificationBot"
                    channel_id = slack_event["channel"]

                    if len(user_message) > 0:
                        data = urllib.parse.urlencode(
                            (
                                ("token", BOT_TOKEN),
                                ("channel", channel_id),
                                ("text", bot_reply)
                            )
                        )
                        data = data.encode("ascii")
                        request = urllib.request.Request(SLACK_URL, data=data, method="POST")
                        request.add_header(
                            "Content-Type",
                            "application/x-www-form-urlencoded"
                        )
                        urllib.request.urlopen(request).read()
                        response = {'status_code': 200}
        logger.info("Response: {}".format(response))
        return response
    except BaseException as err:
        logger.error(err)
