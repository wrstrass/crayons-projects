#!/bin/bash

uvicorn main:app --reload --host 0.0.0.0 --port ${BACKEND_PORT}
