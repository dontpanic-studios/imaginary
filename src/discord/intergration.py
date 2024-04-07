import discordsdk as sdk
import time

actic = sdk.Discord(1226317055356309504, sdk.CreateFlags.default)
activityManager = actic.get_activity_manager()

activity = sdk.Activity()
activity.state = 'Running Through Debugging'
activity.party.id = "00000000"
activity.name = 'Imaginary'


def callback(result):
    if result == sdk.Result.ok:
        print("Successfully set the activity!")
    else:
        raise Exception(result)

activityManager = actic.get_activity_manager().update_activity(activity, callback)

def runcallback():
    while 1:
        time.sleep(1/10)
        actic.run_callbacks()

runcallback()        