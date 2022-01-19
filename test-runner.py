#!/usr/bin/env python3

# CIF test runner
# ---------------
# This is a program that runs each test image through a decoder automatically, to test for
# standards compliance.
# Each image test contains a `test:description` metadata key that describes what the test is about.

import argparse
import os
import shutil
import subprocess

from PIL import Image

ap = argparse.ArgumentParser(description="CIF test runner")
ap.add_argument("decoder", help="the decoder program", nargs='*')
ap.add_argument("--cache_directory", help="directory for cache files", default="_cif_out")
args = ap.parse_args()

cache_directory = os.path.realpath(args.cache_directory)
shutil.rmtree(cache_directory, ignore_errors=True)
os.mkdir(cache_directory)

def print_separator():
   print("--------------------------------")


def run_image_tests(program, directory, check):
   global args, cache_directory

   print_separator()

   n_tests = 0
   results = {}
   for filename in os.listdir(directory):
      input_filename = os.path.realpath(os.path.join(directory, filename))
      basename, ext = os.path.splitext(filename)
      if ext == ".cif":
         output_filename = os.path.join(cache_directory, f"{directory}.{filename}.png")
         testname = os.path.basename(input_filename)
         print(f"{directory} :: {testname}... ", end="")
         command_result = subprocess.run(
            program + [input_filename, output_filename],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
         )
         ok, err = check(command_result, os.path.join(directory, basename), output_filename)
         print("PASSED" if ok else f"FAILED: {err}")
         if ok:
            results[f"{directory}/{testname}"] = True
         n_tests += 1

   print(f"Results for suite '{directory}': {len(results)}/{n_tests} passed ({len(results)/n_tests:.0%})")

   return results, n_tests

print(f"Testing decoder {args.decoder}")
print(f"Using cache directory {cache_directory}")

def check_valid(result, basepath, output_filename):
   if result.returncode != 0:
      return False, "The process returned with a non-zero exit code"

   try:
      reference_image = Image.open(f"{basepath}.png").convert("RGBA")
      result_image = Image.open(output_filename).convert("RGBA")
      if list(reference_image.getdata()) != list(result_image.getdata()):
         return False, "The decoder's result did not match the reference image"
   except Exception as e:
      return False, f"Exception caught while verifying image: {str(e)}"

   return True, None

valid_results, total_valid = run_image_tests(args.decoder, "valid", check_valid)

def check_invalid(result, basepath, output_filename):
   # This will make sure that signals are not interpreted as valid, as they produce negative
   # return codes.
   if result.returncode < 0:
      return False, "The process returned with a signal"
   elif result.returncode == 0:
      return False, "The process succeeded at decoding an invalid image"
   else:
      return True, None
invalid_results, total_invalid = run_image_tests(args.decoder, "invalid", check_invalid)

print_separator()

valid_results, invalid_results = len(valid_results), len(invalid_results)

rating = "Non-compliant"
if valid_results == total_valid and invalid_results == total_invalid:
   print("Congratulations! The decoder passed the full test suite.\n"
      "Contact @liquidev (https://github.com/liquidev) to get your Gold rating.")
   rating = "Silver"
elif valid_results == total_valid:
   print("Sweet! The decoder passed all valid image tests, but its error handling was subpar.\n"
      "Keep on improving your decoder to reach Silver.")
   rating = "Bronze"
else:
   print("Too bad! The decoder does not comply to the CIF specification on an adequate level.\n"
      "Keep on improving your decoder to reach Bronze.")
print(f"Decoder rating: {rating}")
