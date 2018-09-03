#!/bin/bash
LOGFILE="log.txt"

function track {
	case $1 in
		"start")
			# check if LOGFILE exists, if not then create new:
			if [ ! -f LOGFILE ]; 
			then
				echo "START $(date)" > LOGFILE
				echo "LABEL $2" >> LOGFILE

			# check if we already stated a task, if not then update LOGFILE:
			else
				words=$( tail -n 1 LOGFILE )
				words=${words:0:5}
				if [ "$words" == "LABEL" ]; 
				then
					echo "You already have a task ongoing!"
				else
					echo "START $(date)" >> LOGFILE
					echo "LABEL $2" >> LOGFILE
				fi
			fi
			;;

		"status")
			# check if LOGFILE exists:
			if [ ! -f LOGFILE ]; 
			then
				echo "You have not started any task!"
			# check if a task is ongoing or not:
			else
				words=$( tail -n 1 LOGFILE )
				words=${words:0:5}
				if [ "$words" == "LABEL" ]; 
				then
					task=$( tail -n 1 LOGFILE )
					echo "Ongoing: $task"
				else 
					echo "No task ongoing!"
				fi
			fi
			;;

		"stop")
			# check if LOGFILE exists:
			if [ ! -f LOGFILE ]; 
			then
				echo "You have not started any task!"
			# check if a task is ongoing, so we can stop it:
			else
				words=$( tail -n 1 LOGFILE )
				words=${words:0:5}
				if [ "$words" == "LABEL" ];
				then
					echo "Task stopped!"
					echo "END $(date)" >> LOGFILE
					echo " " >> LOGFILE
				else 
					echo "No task ongoing!"
				fi

			fi
			;;

		*)
			echo "To use program you have to type:"
			echo "To start a task: track start name_of_task"
			echo "To check status: track status"
			echo "To end a task: track stop"
			;;
  	esac
}
