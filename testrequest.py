#!/usr/bin/python
import json
import boto3

swf = boto3.client('swf')

DOMAIN = "yourtestdomain"
WORKFLOW = "yourtestworkflow"
VERSION = "0.1"
DECISION_TASKLIST = "decision_tasklist"
ACTIVITY_TASKLIST = "activity_tasklist"

response = swf.start_workflow_execution(
  domain=DOMAIN,
  workflowId='test-1001',
  workflowType={
    "name": WORKFLOW,
    "version": VERSION
  },
  taskList={
      'name': DECISION_TASKLIST
  },
  input=''
)

print "Workflow requested: ", json.dumps(response, indent=4)

'''
Workflow requested:  
{u'runId': u'22OJLNQxEQBLvh8s1h2wceZzmP71g8NWnf2dcWtdWY5I4=', 
'ResponseMetadata': {
  'HTTPStatusCode': 200, 
  'RequestId': 'e6680e70-513e-11e6-979b-490e2c24215c', 
  'HTTPHeaders': {
    'x-amzn-requestid': 'e6680e70-513e-11e6-979b-490e2c24215c', 
    'content-length': '58', 
    'content-type': 'application/x-amz-json-1.0'
    }
  }
}

'''
