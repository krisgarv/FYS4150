#!/bin/bash

climb(){
  if [ $# == 1 ]; then
    for ((i=1;i<=$1;++i)); do
      cd .. ; done
    echo "You have successfully climbed $1 directories up!"
  elif [ $# -gt 1 ]; then
    echo "Cannot interpret input arguments, please state only one integer."
  else
    cd ..
  fi
}
