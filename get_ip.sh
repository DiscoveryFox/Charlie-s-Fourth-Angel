#!/bin/bash
link=$(curl -s -N http://127.0.0.1:4040/api/tunnels | grep -o 'https://[^/"]*\.ngrok.io')
echo "$link"