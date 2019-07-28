#!/usr/bin/env python3

import subprocess

def exec(command):
    return subprocess.run(command, capture_output=True)

def json(result):
    return {
        'stdout': result.stdout.decode('utf-8'),
        'stderr': result.stderr.decode('utf-8'),
        'retcode': result.returncode
    }

from flask import Flask

app = Flask(__name__)

@app.route('/')
def root():
    return json(exec(['./wrapper.sh', 'hello']))

@app.route('/job/<scriptname>', methods=['GET','POST'])
def job_create(scriptname):
    return json(exec(['./wrapper.sh', 'job_create', scriptname]))

@app.route('/job/<id>/status')
def job_status(id):
    return json(exec(['./wrapper.sh', 'job_status', id]))

@app.route('/job/<id>/output')
@app.route('/job/<id>/output/<start>')
@app.route('/job/<id>/output/<start>/<end>')
def job_output(id, start=1, end=0):
    return json(exec(['./wrapper.sh', 'job_output', id, str(start), str(end)]))

@app.route('/job/<id>/output/last')
def job_output_last(id):
    return job_output(id, 0, 0)

@app.route('/job/<id>/remove')
def job_remove(id):
    return json(exec(['./wrapper.sh', 'job_remove', id]))

app.run(host='0.0.0.0')
