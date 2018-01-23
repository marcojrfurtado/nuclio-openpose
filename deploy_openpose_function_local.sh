#!/bin/bash

OPENPOSE_FUNCTION_DIR=./openpose_function

nuctl deploy openpose \
	--platform local \
	--path ${OPENPOSE_FUNCTION_DIR} \
	--no-pull \
	--verbose
