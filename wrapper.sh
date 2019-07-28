#!/bin/bash
# wrapper.sh funcname
#   job_create scriptname
#   job_status id
#   job_output id start end
#   job_remove id

funcname=$1
shift

#tmux=$(which tmux)
[ -z "$tmux" ] && screen=$(which screen)

hello() {
  echo 'hello world'
}

job_create() {
  scriptname=$1
  id=$(uuidgen)
  if [ -n "$tmux" ]; then
    tmux new-session -s $id -d
    tmux send-keys -t $id "./${scriptname}.sh >/var/tmp/${id}.out 2>&1 & echo \$! >/var/tmp/${id}.pid" C-m
  fi
  if [ -n "$screen" ]; then
    screen -S $id -d -m
    screen -S $id -X stuff "./${scriptname}.sh >/var/tmp/${id}.out 2>&1 & echo \$! >/var/tmp/${id}.pid"^M
  fi
  echo $id
}

job_status() {
  id=$1
  if [ -f /var/tmp/${id}.pid ]; then
    if kill -0 $(cat /var/tmp/${id}.pid); then
      status=Running
    else
      status=Done
    fi
  else
    status=Error
  fi
  echo $status
}

job_status_old() {
  id=$1
  rm -f /var/tmp/${id}.job
  tmux send-keys -t $id "jobs %1 >/var/tmp/${id}.job 2>&1" C-m
  if [ $? != 0 ]; then
    status=Error
  else
    while [ ! -f /var/tmp/${id}.job ]; do sleep 0.1; done
    # [1]+  Running
    # [1]+  Done
    if [ -s /var/tmp/${id}.job ]; then
      status=$(sed 's/\[1\]+ *\([^ ]*\) .*/\1/g' /var/tmp/${id}.job)
    else
      status=Done
    fi
  fi
  echo $status
}

job_output() {
  id=$1
  start=$2
  end=$3
  if [ -f /var/tmp/${id}.out ]; then
    if (( $end == 0 )); then
      end=$(wc -l < /var/tmp/${id}.out)
    fi
    if (( $start == -1 )); then
      # reset last
      start=0
      echo 0>/var/tmp/${id}.end
    fi
    if (( $start == 0 )); then
      # last output
      start=$(expr $(cat /var/tmp/${id}.end 2>/dev/null) + 1)
      echo $end >/var/tmp/${id}.end
    fi
    echo $start $end
    sed -n "${start},${end}p; ${end}q" /var/tmp/${id}.out
  fi
}

job_remove() {
  id=$1
  if [ -n "$tmux" ]; then
    tmux kill-session -t $id
    retcode=$?
  fi
  if [ -n "$screen" ]; then
    screen -S $id -X quit >/dev/null
    retcode=$?
  fi
  rm -f /var/tmp/${id}.*
  echo $retcode
}

if [ -n "$funcname" ]; then
  $funcname $*
fi
