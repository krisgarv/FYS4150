#!/bin/bash

boolean=$(mktemp) && echo "true" >$boolean
n=$(mktemp) && declare -i l=1; echo $l >$n
task=$(mktemp) && echo " " >$task

case $1 in

  start)

    if [ $(cat $boolean) = "true" ]; then
      START="START: $(date -u)"
      echo $START

      echo "false" >$boolean
      echo $(cat $boolean)
      if [ $# -gt 1 ]; then
          name="${@:2}"
          echo "Tracking task: $name"
          echo $name >$task
      else
          echo "number $n" >$task
          echo "Tracking task number: $(cat $n)"
      fi
      echo $(cat $n)+1 >$n
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

    if [ $(cat $boolean) = "true" ]; then
      echo "No task tracked at the moment."
    else
      echo "Current task: $task"
    fi
    ;;

  *)
    echo "Bad Usage: Please state <start taskname>, <stop> \
or <status> for your task to be tracked."
    ;;
esac
