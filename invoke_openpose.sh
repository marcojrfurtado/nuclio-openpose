#!/bin/bash
# Invoke openpose and filter only response body
nuctl invoke openpose -c "text/plain" -b "$1" -m POST --platform local | sed '1,/body/d'
