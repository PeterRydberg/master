#!/bin/bash
srun -N1 -n1 -c2 --mem-per-cpu=1024 --partition=HEID --gres=gpu:1 -w heid --pty bash
