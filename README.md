# API-to-Shell

## Installation

```
yum install tmux
# OR
yum install screen
```

```
pip install flask

./server.py
```

## API

CREATE: 
http://localhost:5000/job/test2

GET STATUS: 
http://localhost:5000/job/{{jobid}}/status

LAST OUTPUT: 
http://localhost:5000/job/{{jobid}}/output/last

REMOVE: 
http://localhost:5000/job/{{jobid}}/remove
