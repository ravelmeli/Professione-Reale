#!/bin/bash
cd /home/user/Professione-Reale/remotion
TOTAL=16571
STEP=1500
i=0
for ((a=0; a<TOTAL; a+=STEP)); do
  b=$((a+STEP-1)); if [ $b -ge $TOTAL ]; then b=$((TOTAL-1)); fi
  f=out/chunks/c$(printf %02d $i).mp4
  if [ ! -f "$f" ]; then
    npx remotion render src/index.ts Full "$f.part.mp4" --frames=$a-$b --muted --concurrency=3 --codec=h264 --crf=20 --image-format=jpeg --jpeg-quality=88 2>&1 | tail -n 3
    mv "$f.part.mp4" "$f"
  fi
  echo "chunk $i done $(date +%T)"
  i=$((i+1))
done
echo ALLDONE
