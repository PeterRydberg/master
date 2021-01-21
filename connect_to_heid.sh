#!/bin/bash

while getopts t:g: flag; do
    case "${flag}" in
    t) TIME_LIMIT=${OPTARG} ;;  # e.g. 12:00:00
    g) GPUS=${OPTARG} ;;  # gpu:2
    esac
done

srun -N1 -n1 -c2 --mem-per-cpu=1024 --partition=HEID --gres=$GPUS --time=$TIME_LIMIT -w heid --pty bash
