#!/bin/bash

boolean=$(mktemp) && echo "true" >$boolean
n=1
task=""

case $1 in

  start)

    if [ $(cat $boolean) = "true" ]; then
      START="START: $(date -u)"
      echo $START
      echo "false" >$boolean
      echo $(cat $boolean)
      if [ $# -gt 1 ]; then
          task="${@:2}"
          echo "Tracking task: $task"
      else
        echo "Tracking task number: $n"
      fi
      ((n++))
      exit
    else
      echo "Please stop current task before you start a new one."
    fi
    ;;

  stop)

    if [ $(cat $boolean) = "false" ]; then
      STOP="STOP: $(date -u)"
      echo $STOP
      echo "true" >$boolean
      echo $(cat $boolean)
      exit
    else
      echo "No task tracked at the moment."
    fi
    ;;

  status)
    if [ $Available ]; then
      echo "No task tracked at the moment."
    else
      echo "Current task: $task"
    fi
    ;;

  *)
    echo "Bad Usage: Please state <start taskname>, <stop> \
    or <status> for your task to be tracked"
    ;;
esac
