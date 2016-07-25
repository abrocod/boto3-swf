#!/usr/bin/python

import boto3
from botocore.exceptions import ClientError

DOMAIN = "yourtestdomain"
WORKFLOW = "yourtestworkflow"
VERSION = "0.1"
DECISION_TASKLIST = "decision_tasklist"
ACTIVITY_TASKLIST = "activity_tasklist"

swf = boto3.client('swf')

try:
  swf.register_domain(
    name=DOMAIN,
    description="Test SWF domain",
    workflowExecutionRetentionPeriodInDays="10"
  )
except ClientError as e:
  print "Domain already exists: ", e.response.get("Error", {}).get("Code")

try:
  swf.register_workflow_type(
    domain=DOMAIN,
    name=WORKFLOW,
    version=VERSION,
    description="Test workflow",
    defaultExecutionStartToCloseTimeout="250",
    defaultTaskStartToCloseTimeout="NONE",
    defaultChildPolicy="TERMINATE",
    defaultTaskList={"name": DECISION_TASKLIST}
  )
  print "Test workflow created!"
except ClientError as e:
  print "Workflow already exists: ", e.response.get("Error", {}).get("Code")

try:
  swf.register_activity_type(
    domain=DOMAIN,
    name="task_A",
    version=VERSION,
    description="Test worker",
    defaultTaskStartToCloseTimeout="NONE",
    defaultTaskList={"name": ACTIVITY_TASKLIST}
  )
  print "Test worker created!"
except ClientError as e:
  print "Activity already exists: ", e.response.get("Error", {}).get("Code")

try:
  swf.register_activity_type(
    domain=DOMAIN,
    name="task_B",
    version=VERSION,
    description="Test worker",
    defaultTaskStartToCloseTimeout="NONE",
    defaultTaskList={"name": ACTIVITY_TASKLIST}
  )
  print "Test worker created!"
except ClientError as e:
  print "Activity already exists: ", e.response.get("Error", {}).get("Code") 


