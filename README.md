Server Side FCM push notification sending example.

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