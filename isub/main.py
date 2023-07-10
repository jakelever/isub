#!/usr/bin/env python3

import argparse
import os
from datetime import datetime
import random
import string
import tempfile
import time
from subprocess import run
import inspect
import isub

def main():
	default_image = 'jakelever/ml_gpu:latest'
	gpu_options = ['none','titan','2080ti','a6000','3090']

	parser = argparse.ArgumentParser("Tool for running jobs on OpenShift cluster",
									formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--script',required=False,type=str,help='Bash script to run')
	parser.add_argument('--command',required=False,type=str,help='Command to run')
	parser.add_argument('--printonly',action='store_true',help='Print out the job file to stdout (useful for debug) and do not submit')
	parser.add_argument('--name',required=False,type=str,help='Name to give the job')
	parser.add_argument('--logfile',required=False,type=str,help='Output name of log file (where stdout/stderr will be piped). If not provided, one will be creating using the job id')
	parser.add_argument('--image',required=False,type=str,default=default_image,help='Docker image to use')
	parser.add_argument('--cpu',required=False,type=int,default=2,help='How many CPUs to request')
	parser.add_argument('--mem',required=False,type=int,default=8,help='How much memory to request (in GiB)')
	parser.add_argument('--gpu',required=False,type=str,default='3090',help=f'Which GPU to request (options are {", ".join(gpu_options)}.')
	args = parser.parse_args()

	assert args.script or args.command, "Must provide --script with a Bash script or --command with a shell command"

	username = os.environ['USER']

	volume_directory = f'/home/{username}/{username}vol1claim'
	assert os.path.isdir(volume_directory), f"Could not find expected directory: {volume_directory}. Unable to launch job"
	
	base_dir = os.path.dirname(inspect.getfile(isub))
	base_dir = base_dir.replace(os.path.realpath(volume_directory), volume_directory)
	template_filename = f'{base_dir}/template.yml'
	
	assert os.path.isfile(template_filename), "Unable to find the template file"

	if args.command:
		run_script = f'{base_dir}/run_command.sh'
		run_args = args.command
	elif args.script:
		assert os.path.isfile(args.script)

		run_script = f'{base_dir}/run_script.sh'
		run_args = args.script


	assert args.gpu in gpu_options

	cpu_text = f"{args.cpu}000m"
	mem_text = f"{args.mem}Gi"

	if args.gpu == 'none':
		gpu_count = ''
		gpu_type = ''
	else:
		gpu_count = 'nvidia.com/gpu: 1'
		gpu_type = f'node-role.ida/gpu{args.gpu}: "true"'

	pwd = os.environ['PWD']

	#permissions_for_cwd = oct(os.stat(os.getcwd()).st_mode)
	#print(permissions_for_cwd)
	print("WARNING: Not checking for permissions. Will be implemented!")

	now = datetime.now()
	job_date = now.strftime("%Y-%m-%d-%H-%M-%S")
	rand_id = "".join(random.choices(string.ascii_lowercase,k=4))
	job_id = f"{job_date}-{rand_id}"

	if args.name:
		job_name = f"{args.name}-{job_id}"
	elif args.script:
		job_name = f"{args.script[0]}-{job_id}"
	else:
		first_part_of_command = args.command.strip().split()[0]
		job_name = f"{first_part_of_command}-{job_id}"

	allowed_chars = string.ascii_letters + string.digits + '-'
	job_name = job_name.lower().replace('/','-')
	job_name = "".join( c for c in job_name if c in allowed_chars )

	if args.logfile:
		logfile = args.logfile
	else:
		logfile = f"log.{job_id}.out"

	with open(template_filename) as f:
		template = f.read()

	template = template.replace('<USERNAME>',username)
	template = template.replace('<JOB_NAME>',job_name)
	template = template.replace('<JOB_ID>',job_id)
	template = template.replace('<WORKING_DIR>',pwd)
	template = template.replace('<RUN_SCRIPT>',run_script)
	template = template.replace('<RUN_ARGS>',run_args)
	template = template.replace('<LOGFILE>',logfile)
	template = template.replace('<CPU>',cpu_text)
	template = template.replace('<MEMORY>',mem_text)
	template = template.replace('<GPU_COUNT>',gpu_count)
	template = template.replace('<GPU_TYPE>',gpu_type)

	if args.printonly:
		print(template)
		return

	with tempfile.NamedTemporaryFile() as tf:
		with open(tf.name,'w') as f:
			f.write(template)

		p = run(['oc','create','-f',tf.name])
		assert p.returncode == 0, f"oc return code = {p.returncode}"

if __name__ == '__main__':
	main()

