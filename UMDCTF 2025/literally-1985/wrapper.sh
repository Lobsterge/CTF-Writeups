#!/bin/bash
TMPDIR="$(mktemp -d)"
echo "Enter file contents, ended with the string EOF:"
while IFS= read -r line; do
    if [ "$line" == "EOF" ]; then
        break
    fi
    echo "$line" >> $TMPDIR/script.js
done
./d8 --allow-natives-syntax $TMPDIR/script.js
