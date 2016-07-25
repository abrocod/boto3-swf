#!/usr/bin/python

import boto3
from botocore.client import Config
import uuid
import json

botoConfig = Config(connect_timeout=50, read_timeout=70)
swf = boto3.client('swf', config=botoConfig)

DOMAIN = "yourtestdomain"
WORKFLOW = "yourtestworkflow"
VERSION = "0.1"
DECISION_TASKLIST = "decision_tasklist"
ACTIVITY_TASKLIST = "activity_tasklist"

print "Listening for Decision Tasks"

while True:

  newTask = swf.poll_for_decision_task(
    domain=DOMAIN,
    taskList={'name': DECISION_TASKLIST},
    identity='decider-1',
    reverseOrder=False)

  if 'taskToken' not in newTask:
    print "Poll timed out, no new task.  Repoll"

  elif 'events' in newTask:

    eventHistory = [evt for evt in newTask['events'] if not evt['eventType'].startswith('Decision')]
    lastEvent = eventHistory[-1]

    print '---- one iteration -----'
    # for _event in eventHistory:
    #   print '[INFO]', _event
    print '[LAST_EVENT] ', lastEvent

    if lastEvent['eventType'] == 'WorkflowExecutionStarted':
      print "Dispatching task to worker", newTask['workflowExecution'], newTask['workflowType']
      
      swf.respond_decision_task_completed(
        taskToken=newTask['taskToken'],
        decisions=[
          {
            'decisionType': 'ScheduleActivityTask',
            'scheduleActivityTaskDecisionAttributes': {
                'activityType':{
                    'name': TASKNAME,
                    'version': VERSION
                    },
                'activityId': 'activityid-' + str(uuid.uuid4()),
                'input': '',
                'scheduleToCloseTimeout': 'NONE',
                'scheduleToStartTimeout': 'NONE',
                'startToCloseTimeout': 'NONE',
                'heartbeatTimeout': 'NONE',
                'taskList': {'name': DECISION_TASKLIST},
            }
          }
        ]
      )
      print "Task Dispatched:", newTask['taskToken']

    elif lastEvent['eventType'] == 'ActivityTaskCompleted':
      swf.respond_decision_task_completed(
        taskToken=newTask['taskToken'],
        decisions=[
          {
            'decisionType': 'CompleteWorkflowExecution',
            'completeWorkflowExecutionDecisionAttributes': {
              'result': 'success'
            }
          }
        ]
      )
      print "Task Completed!"


'''
Dispatching task to worker {
u'workflowId': u'test-1001', 
u'runId': u'22OJLNQxEQBLvh8s1h2wceZzmP71g8NWnf2dcWtdWY5I4='} {
u'version': u'0.1', 
u'name': u'yourtestworkflow'}


Task Dispatched: AAAAKgAAAAIAAAAAAAAAAgl6hgh1Dh02zrVzq7c9Don6n9W2bWLiw3oNjDS6zx3lqGaUTZK+O1ZhjalBdnPRKEi2w7sNua3msaM4cIeqRhzHLUYfCgFKQdz2t/luS0LPGDRTbtGhkA9nyEyf1sBCv/+fyvQJwl79fxoJcXdmo4nS8+odc88VArGWCT2JzBLEkBbkSJE8Bf6V7WbK33eejMwZq3aKIhpvS/WAPdilnO+hmAKoOjFOSivmuWR8k/f8ShbLSrnCdaypM86HspYvlZQy2z6tPsG+0b3n7h10NN0qRkh1qf8SkHFJcbBBvooc

Task Completed!
'''

'''
[INFO] {
u'eventId': 1, 
u'eventType': u'WorkflowExecutionStarted', 
u'workflowExecutionStartedEventAttributes': {
  u'taskList': {u'name': u'testlist'}, 
  u'parentInitiatedEventId': 0, 
  u'taskStartToCloseTimeout': u'NONE', 
  u'childPolicy': u'TERMINATE', 
  u'executionStartToCloseTimeout': u'250', 
  u'input': u'', 
  u'workflowType': {
    u'version': u'0.1', 
    u'name': u'yourtestworkflow'
    }
  }, 
  u'eventTimestamp': datetime.datetime(2016, 7, 23, 21, 49, 21, 307000, tzinfo=tzlocal())
}

'''

"""
[INFO] {u'eventId': 1, u'eventType': u'WorkflowExecutionStarted', u'workflowExecutionStartedEventAttributes': {u'taskList': {u'name': u'testlist'}, u'parentInitiatedEventId': 0, u'taskStartToCloseTimeout': u'NONE', u'childPolicy': u'TERMINATE', u'executionStartToCloseTimeout': u'250', u'input': u'', u'workflowType': {u'version': u'0.1', u'name': u'yourtestworkflow'}}, u'eventTimestamp': datetime.datetime(2016, 7, 23, 22, 26, 29, 584000, tzinfo=tzlocal())}
Dispatching task to worker {u'workflowId': u'test-1001', u'runId': u'22HEw6YNd0rMlI3yTf5bjUsyvNGtCjtkNVL/KbUqMZlT8='} {u'version': u'0.1', u'name': u'yourtestworkflow'}
Task Dispatched: AAAAKgAAAAIAAAAAAAAAAh02gfFKlgKwJheUdLtBOt+tdF0EEv2g0uMjoz9Vj+MT89OE8GVJ2cRRdXkvGTxRLSoj7TFQWjUkXhPavvrdf3RGYAd0RWWouay2nVmuP7WZ4HhUkFEZ6zC3hUHvjm/tvNJIa92qdBYEWkoBtCeqQY+BLUZkcbgbxdnegAUfeTc62bSsnnqijS6o6mbzrWKAf12CwWhESVAE6Yo+OtEU+uiZ2RlWmwLI4YcALnQXP6xmqc6QIH/+diSymjHWZAkoqmdsriDDvWGkH67BC355iMwthJjaW+ZN5FfU/SQu4IRw
[INFO] {u'eventId': 1, u'eventType': u'WorkflowExecutionStarted', u'workflowExecutionStartedEventAttributes': {u'taskList': {u'name': u'testlist'}, u'parentInitiatedEventId': 0, u'taskStartToCloseTimeout': u'NONE', u'childPolicy': u'TERMINATE', u'executionStartToCloseTimeout': u'250', u'input': u'', u'workflowType': {u'version': u'0.1', u'name': u'yourtestworkflow'}}, u'eventTimestamp': datetime.datetime(2016, 7, 23, 22, 26, 29, 584000, tzinfo=tzlocal())}
[INFO] {u'eventId': 5, u'eventType': u'ActivityTaskScheduled', u'activityTaskScheduledEventAttributes': {u'taskList': {u'name': u'testlist'}, u'scheduleToCloseTimeout': u'NONE', u'activityType': {u'version': u'0.1', u'name': u'yourtaskname'}, u'decisionTaskCompletedEventId': 4, u'heartbeatTimeout': u'NONE', u'activityId': u'activityid-d8faacbb-3b54-4c56-a357-8459635ac20a', u'scheduleToStartTimeout': u'NONE', u'startToCloseTimeout': u'NONE', u'input': u''}, u'eventTimestamp': datetime.datetime(2016, 7, 23, 22, 26, 29, 721000, tzinfo=tzlocal())}
[INFO] {u'eventId': 6, u'eventType': u'ActivityTaskStarted', u'eventTimestamp': datetime.datetime(2016, 7, 23, 22, 26, 29, 797000, tzinfo=tzlocal()), u'activityTaskStartedEventAttributes': {u'scheduledEventId': 5, u'identity': u'worker-1'}}
[INFO] {u'eventId': 7, u'eventType': u'ActivityTaskCompleted', u'activityTaskCompletedEventAttributes': {u'startedEventId': 6, u'scheduledEventId': 5, u'result': u'success'}, u'eventTimestamp': datetime.datetime(2016, 7, 23, 22, 26, 29, 835000, tzinfo=tzlocal())}
Task Completed!

"""

