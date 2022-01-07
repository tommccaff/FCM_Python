"""Server Side FCM push notification sending example.

Firebase Cloud Messaging (FCM) can be used to send messages to clients on iOS,
Android and Web, using the Firebase Admin SDK and the Firebase messages:send API.
This example was originally taken from https://github.com/firebase/quickstart-python
and modified using my actual project and other settings inserted to create a working
example.  Note that it also requires the .json file that is obtained by selecting
`Python` and clicking `Generate new private key` from the service accounts tab of
the Firebase project settings.  This .json file must reside in the same directory as
this Python script.

This example uses FCM to send two types of messages to clients that are subscribed
to the `STUDENTS` topic. One type of message is a simple notification message (display message).
The other is a notification message (display notification) with platform specific
customizations. For example, a badge is added to messages that are sent to iOS devices.
Note that only Android devices have been tested.

The receiving Flutter app must have subscribed to the `STUDENTS` topic.  This can
be done using the following code:

FirebaseMessaging.instance.subscribeToTopic('STUDENTS');


This Python script can be called from a command prompt as follows:

python messaging.py --message=common-message
or
python messaging.py --message=override-message

"""

import argparse
import json
import requests

from oauth2client.service_account import ServiceAccountCredentials

PROJECT_ID = 'pushapijava'
CREDENTIALS_JSON_KEYFILE = 'pushapijava-firebase-adminsdk-ngjtn-2bc0730dfb.json'

BASE_URL = 'https://fcm.googleapis.com'
FCM_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/messages:send'
FCM_URL = BASE_URL + '/' + FCM_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

# [START retrieve_access_token]
def _get_access_token():
  """Retrieve a valid access token that can be used to authorize requests.

  :return: Access token.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      CREDENTIALS_JSON_KEYFILE, SCOPES)
  access_token_info = credentials.get_access_token()
  return access_token_info.access_token
# [END retrieve_access_token]

def _send_fcm_message(fcm_message):
  """Send HTTP request to FCM with given message.

  Args:
    fcm_message: JSON object that will make up the body of the request.
  """
  # [START use_access_token]
  headers = {
    'Authorization': 'Bearer ' + _get_access_token(),
    'Content-Type': 'application/json; UTF-8',
  }
  # [END use_access_token]
  resp = requests.post(FCM_URL, data=json.dumps(fcm_message), headers=headers)

  if resp.status_code == 200:
    print('Message sent to Firebase for delivery, response:')
    print(resp.text)
  else:
    print('Unable to send message to Firebase')
    print(resp.text)

def _build_common_message():
  """Construct common notifiation message.

  Construct a JSON object that will be used to define the
  common parts of a notification message that will be sent
  to any app instance subscribed to the news topic.
  """
  return {
    'message': {
      'topic': 'STUDENTS',
      'notification': {
        'title': 'FCM Notification from Python',
        'body': 'Python sending to STUDENTS topic'
      }
    }
  }

def _build_override_message():
  """Construct common notification message with overrides.

  Constructs a JSON object that will be used to customize
  the messages that are sent to iOS and Android devices.
  """
  fcm_message = _build_common_message()

  apns_override = {
    'payload': {
      'aps': {
        'badge': 1
      }
    },
    'headers': {
      'apns-priority': '10'
    }
  }

  android_override = {
    'notification': {
      'click_action': 'android.intent.action.MAIN'
    }
  }

  fcm_message['message']['android'] = android_override
  fcm_message['message']['apns'] = apns_override

  return fcm_message

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--message')
  args = parser.parse_args()
  if args.message and args.message == 'common-message':
    common_message = _build_common_message()
    print('FCM request body for message using common notification object:')
    print(json.dumps(common_message, indent=2))
    _send_fcm_message(common_message)
  elif args.message and args.message == 'override-message':
    override_message = _build_override_message()
    print('FCM request body for override message:')
    print(json.dumps(override_message, indent=2))
    _send_fcm_message(override_message)
  else:
    print('''Invalid command. Please use one of the following commands:
python messaging.py --message=common-message
python messaging.py --message=override-message''')

if __name__ == '__main__':
  main()
