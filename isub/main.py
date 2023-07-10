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
	gpu_options = ['none','titan','2080ti','a6000','3090']

	parser = argparse.ArgumentParser("Tool for running jobs on OpenShift cluster",
									formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('script',nargs='+',type=str,help='Script to run')
	parser.add_argument('--command',action='store_true',help='Run the arguments as a command and not a script')
	parser.add_argument('--print',action='store_true',help='Print out the job file to stdout (useful for debug)')
	parser.add_argument('--name',required=False,type=str,help='Name to give the job')
	parser.add_argument('--cpu',required=False,type=int,default=2,help='How many CPUs to request')
	parser.add_argument('--mem',required=False,type=int,default=8,help='How much memory to request (in GiB)')
	parser.add_argument('--gpu',required=False,type=str,default='3090',help=f'Which GPU to request (options are {", ".join(gpu_options)}.')
	args = parser.parse_args()
	
	base_dir = os.path.dirname(inspect.getfile(isub))
	template_filename = f'{base_dir}/template.yml'
	
	assert os.path.isfile(template_filename), "Unable to find the template file"

	if args.command:
		run_script = f'{base_dir}/run_command.sh'
		run_args = ' '.join(args.script)
	else:
		assert len(args.script) == 1, "Expected a single script file"
		assert os.path.isfile(args.script[0])

		run_script = f'{base_dir}/run_script.sh'
		run_args = args.script[0]


	assert args.gpu in 

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
	else:
		job_name = f"{args.script[0]}-{job_id}"

	allowed_chars = string.ascii_letters + string.digits + '-'
	job_name = job_name.lower().replace('/','-')
	job_name = "".join( c for c in job_name if c in allowed_chars )

	with open(template_filename) as f:
		template = f.read()

	template = template.replace('<JOB_NAME>',job_name)
	template = template.replace('<JOB_ID>',job_id)
	template = template.replace('<WORKING_DIR>',pwd)
	template = template.replace('<RUN_SCRIPT>',run_script)
	template = template.replace('<RUN_ARGS>',run_args)
	template = template.replace('<CPU>',cpu_text)
	template = template.replace('<MEMORY>',mem_text)
	template = template.replace('<GPU_COUNT>',gpu_count)
	template = template.replace('<GPU_TYPE>',gpu_type)

	if args.print:
		print(template)

	with tempfile.NamedTemporaryFile() as tf:
		with open(tf.name,'w') as f:
			f.write(template)

		p = run(['oc','create','-f',tf.name])
		assert p.returncode == 0, f"oc return code = {p.returncode}"

if __name__ == '__main__':
	main()

