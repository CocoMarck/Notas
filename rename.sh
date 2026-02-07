#!/bin/bash
for f in ./Note_*.txt; do
  mv "$f" "${f/Note_/nota-}"
done

for f in *.txt; do
  nf="${f,,}"          # todo a minúsculas
  nf="${nf//_/-}"      # _ por -
  nf="${nf// /-}"      # espacios por -
  mv "$f" "$nf"
done

for f in *.txt; do
  nf="${f,,}"            # minúsculas
  nf="${nf//[_ ]/-}"     # _ y espacios → -
  while [[ "$nf" == *"--"* ]]; do
    nf="${nf//--/-}"     # colapsa ---- → -
  done
  mv "$f" "$nf"
done



