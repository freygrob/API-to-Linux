#!/usr/bin/env python3

import shellfuncs
from wrapper import hello, job_create, job_status, job_output, job_remove

from flask import Flask

app = Flask(__name__)

@app.route('/')
def root():
    returncode, stdout, stderr = hello()
    return stdout

@app.route('/job/<scriptname>', methods=['GET','POST'])
def create(scriptname):
    returncode, stdout, stderr = job_create(scriptname)
    return stdout

@app.route('/job/<id>/status')
def status(id):
    returncode, stdout, stderr = job_status(id)
    return stdout

@app.route('/job/<id>/output')
@app.route('/job/<id>/output/<start>')
@app.route('/job/<id>/output/<start>/<end>')
def output(id, start=1, end=0):
    returncode, stdout, stderr = job_output(id, start, end)
    return stdout

@app.route('/job/<id>/output/last')
def output_last(id):
    return output(id, 0, 0)

@app.route('/job/<id>/remove')
def remove(id):
    returncode, stdout, stderr = job_remove(id)
    return stdout

app.run(host='0.0.0.0')
