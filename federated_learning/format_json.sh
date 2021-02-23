
#!/bin/bash

while getopts n: flag; do
    case "${flag}" in
        n) FILE_NAME=${OPTARG} ;;
	esac
    done

jq . $FILE_NAME > temp.json && mv temp.json $FILE_NAME
