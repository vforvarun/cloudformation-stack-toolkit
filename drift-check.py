import boto3
import click

stack_session = boto3.client('cloudformation')

@click.group('cli')
def cli():
    pass

@cli.command('list-stacks')
def list_stack():
   "List the status and drift status of all stacks"

   dash = '-' * 120
   paginator = stack_session.get_paginator('list_stacks')
   response_iterator = paginator.paginate(StackStatusFilter=['CREATE_COMPLETE','UPDATE_COMPLETE'])
   print(dash)
   print('{:<40s}{:>20s}{:>20s}{:>20s}'.format("Stack Name","Stack Status","Drift Status","Last Checked"))
   print(dash)
   for page in response_iterator:
	   stacks = page['StackSummaries']
	   for stack in stacks:
		 if(stack['DriftInformation']['StackDriftStatus'] == "NOT_CHECKED"):
			print('{:<40s}{:>20s}{:>20s}'.format(stack['StackName'],stack['StackStatus'],stack['DriftInformation']['StackDriftStatus']))
		 else:
			print('{:<40s}{:>20s}{:>20s}{:>20s}'.format(stack['StackName'],stack['StackStatus'],stack['DriftInformation']['StackDriftStatus'],stack['DriftInformation']['LastCheckTimestamp'].strftime("%Y-%m-%d %H:%M")))

@cli.command('describe-stack')
@click.argument('stackname')
def describe_stack(stackname):
   "List the status and drift status of a particular stack"

   dash = '-' * 80
   paginator = stack_session.get_paginator('describe_stacks')
   response_iterator = paginator.paginate(StackName=stackname)
   print(dash)
   print('{:<40s}{:>20s}{:>20s}{:>20s}'.format("Stack Name","Stack Status","Drift Status","Last Checked"))
   print(dash)
   for page in response_iterator:
	   stacks = page['Stacks']
	   for stack in stacks:
		 if(stack['DriftInformation']['StackDriftStatus'] == "NOT_CHECKED"):
			print('{:<40s}{:>20s}{:>20s}'.format(stack['StackName'],stack['StackStatus'],stack['DriftInformation']['StackDriftStatus']))
		 else:
			print('{:<40s}{:>20s}{:>20s}{:>20s}'.format(stack['StackName'],stack['StackStatus'],stack['DriftInformation']['StackDriftStatus'],stack['DriftInformation']['LastCheckTimestamp'].strftime("%Y-%m-%d %H:%M")))

@cli.command('detect-stack-drift')
@click.argument('stackname')
def detect_stack_drift(stackname):
	"Trigger drift detect for a particular stack"
	try:
		response = stack_session.detect_stack_drift(StackName=stackname)
		print("Stack Drift Check has been successfully triggered on {:s}".format(stackname))
	except:
	    print("Failed")

@cli.command('detect-stack-drift-all')
def detect_drift_all():
   "Trigger drift detect of all stacks"

   print("Trigger Stack Drift Check on all stacks")

   paginator = stack_session.get_paginator('list_stacks')
   response_iterator = paginator.paginate(StackStatusFilter=['CREATE_COMPLETE','UPDATE_COMPLETE'])
   for page in response_iterator:
	   stacks = page['StackSummaries']
	   for stack in stacks:
		try:
			response = stack_session.detect_stack_drift(StackName = stack['StackName'])
			print("Stack Drift Check has been successfully triggered on the stack {:s}".format(stack['StackName']))
		except:
			print("Failed")


if __name__ == '__main__':
    cli()
