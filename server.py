#!/usr/bin/env python3

import subprocess
def exec(command):
    return subprocess.run(command, capture_output=True)

from flask import Flask

app = Flask(__name__)

@app.route('/')
def root():
    return exec('api-to-shell/hello.sh').stdout

@app.route('/job/<scriptname>', methods=['GET','POST'])
def job_create(scriptname):
    return exec(['./wrapper.sh', 'job_create', scriptname]).stdout

@app.route('/job/<id>/status')
def job_status(id):
    return exec(['./wrapper.sh', 'job_status', id]).stdout

@app.route('/job/<id>/output')
@app.route('/job/<id>/output/<start>')
@app.route('/job/<id>/output/<start>/<end>')
def job_output(id, start=1, end=0):
    return exec(['./wrapper.sh', 'job_output', id, str(start), str(end)]).stdout

@app.route('/job/<id>/output/last')
def job_output_last(id):
    return job_output(id, 0, 0)

@app.route('/job/<id>/remove')
def job_remove(id):
    return exec(['./wrapper.sh', 'job_remove', id]).stdout

app.run(host='0.0.0.0')
