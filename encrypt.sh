#!/bin/bash

echo "Encrypt (e) or decrypt (d)?"
read enc


# # encrypt
if [ "$enc" == "e" ]; then
echo "Filename? (including extention)"
read inName

# take path and give to output
echo "Output name? (including extention)"
read outName
openssl enc -bf -a -salt -in $inName -out $outName.enc
fi

# # decrypt
if [ "$enc" == "d" ]; then
echo "Filename? (including extention)"
read inName
# take path and give to output
echo "Output name? (including desired extention)"
read outName
openssl enc -bf -d -a -in $inName -out $outName
fi
