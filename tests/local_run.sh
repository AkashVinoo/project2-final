#!/usr/bin/env bash
uvicorn main:app --port 8000 &
PID=$!
sleep 2
curl "http://127.0.0.1:8000/api/" -F "questions=@examples/question_wiki.txt;type=text/plain"
kill $PID