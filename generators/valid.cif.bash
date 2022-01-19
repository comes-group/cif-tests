#!/usr/bin/env bash

encoder=$@

make-cifs() {
   for png in $@; do
      cif=$(dirname $png)/$(basename $png .png).cif
      echo $png
      $encoder $png $cif
   done
}

make-cifs "valid/limits*.png"
