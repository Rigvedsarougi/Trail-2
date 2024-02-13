#!/bin/bash

# Push the content to your GitHub repository
git remote set-url origin https://github.com/vitalyis/transcribe-speech2text.git
git push -u origin main

# Create and push the requirements file to an online repository
pip freeze > requirements.txt

git add requirements.txt
git commit -m "Add requirements.txt file"
git push -u origin main