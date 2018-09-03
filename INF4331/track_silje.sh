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
					task=${task:6}
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

		"log")
			# find the time used for each task (printing to terminal):
			for line in `cat LOGFILE`;
			do
				firstword=${line:0:3}
				if [ "$firstword" == "STA" ];
				then
					time1=${line:17:8}

				elif [ "$firstword" == "LAB" ];
				then
					timelab=${line:6}

				elif [ "$firstword" == "END" ];
				then
					time2=${line:15:8}

				elif [ "$firstword" == " " ];
				then
					seconds1=${time1:6:2}
					minutes1=${time1:3:2}
					hours1=${time1:0:2}
					tot_seconds1=$(( ${seconds1}+${minutes1}*60+${hours1}*60*60 ))	

					seconds2=${time2:6:2}
					minutes2=${time2:3:2}
					hours2=${time2:0:2}
					tot_seconds2=$(( ${seconds2}+${minutes2}*60+${hours2}*60*60 ))

					sec_tot=$(( ${tot_seconds2}-${tot_seconds1} ))

					min_tot=0
					hour_tot=0
					while (("sec_tot" > "59"));
					do
						sec_tot=$(( ${sec_tot}-60 ))
						min_tot=$(( ${min_tot}+1 ))
					done
					
					while (("min_tot" > "59"));
					do
						min_tot=$(( ${min_tot}-60 ))
						hour_tot=$(( ${hour_tot}+1 ))
					done
					
					hour_out=$(printf "%02d" $hour_tot)
					min_out=$(printf "%02d" $min_tot)
					sec_out=$(printf "%02d" $sec_tot)
					echo "$timelab: ${hour_out}:${min_out}:${sec_out}"	
				fi
			done
			;;

		*)
			echo "To use program you have to type:"
			echo "To start a task: track start name_of_task"
			echo "To check status: track status"
			echo "To end a task: track stop"
			;;
  	esac
}
