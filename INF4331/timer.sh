#!/bin/bash

Avail="true"
task=""
errormessage="Error: please execute one of the following commands; \
'timer start yourtaskname', 'timer stop' or 'timer status'"
notask="No current task to track"
#declare global variable AVAILABLE!
timer() {
  if [ $# -gt 1 ]; then
      if [ "$1" == "start" ]; then
          if [ $Avail=="true" ]; then
            START="START: $(date -u)"
            $task="${@:2}"
            echo $START >> LOGFILE
            echo "Tracking task: $task"
            $Avail="false"
          else
            echo "Please stop current task before starting \
            a new timer."
          fi
      elif [ "$1" == "stop" ]; then
          if [ $Avail=="false" ]; then
            echo "Task completed: $task"
            STOP="STOP: $(date -u)"
            print STOP
            echo $STOP
            $Avail="true"
            $task="$notask"
          else
            echo "$notask"
          fi
      elif [ "$1"=="status" ]; then
          echo "Current task: $task"
      else
          echo $errormessage
      fi
  else
    echo $errormessage
  fi
} > LOGFILE
