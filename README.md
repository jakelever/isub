# isub: Job submitter for IDA OpenShift cluster

This is a basic system for submitting jobs to the IDA OpenShift GPU cluster. It sets up a job on the cluster using a Docker image and connects to the file system so that your files are accessible.

## Installation

Install using pip3 directly from this GitHub repo

```
pip3 install -U --user git+https://github.com/jakelever/isub.git
```

## Important details

- You can only run code inside your volume directory (something like /home/jakelever/jakelevervol1claim).
- The directories which you write to must be write accessible to all. Use `chmod a+w <DIRECTORY>` with the directory you want to make write accessible to all

## Example Usage

Let's show an example of running some HuggingFace Python code. Create a file called `example.py` with the five lines of Python below. And note the important details above about where you run it and write permissions.

```python
from transformers import pipeline, set_seed
generator = pipeline('text-generation', model="distilgpt2")
set_seed(42)
generated = generator("Hello, I'm a language model,", max_length=30, num_return_sequences=5)
print(generated)
```

You can then run it on the cluster with the `isub` command below. It should create a job that will be visible through the cluster console (link on the cluster Moodle page) and save the output to a log file.

```
isub --command "python3 example.py"
```

## More controls

Run the help command to see all the options. This can give you controls over the resources requested (e.g. GPUs, CPUs, memory), the log file and other useful things.

```
isub --help
```

## Running a script instead of a command

The earlier example runs a Python3 command. You could also save the commands to a `.sh` shell script and use `--script` to run that.

## Custom Docker images

The default Docker image used is `jakelever/ml_gpu` which is set up to work with the different machines and have a basic install of the standard machine learning and deep learning libraries. The Dockerfile for it is in the [docker/](https://github.com/jakelever/isub/tree/main/docker) directory. You could create your own one, upload it to DockerHub and use `--image` to select it.
