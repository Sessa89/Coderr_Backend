git add .
git commit -m "%~1"
git push
ssh phili@35.198.65.76 "cd ~/projects/Coderr_Backend && git pull"