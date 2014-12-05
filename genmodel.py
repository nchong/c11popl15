#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import sys
import subprocess

CHOICES_RF=["ConsRFna","Naive","Arf","Arfna"]
CHOICES_SC=["SCorig","SCnew"]
CHOICES_RS=["RSorig","RSnew"]
CHOICES_ST=["STorig","STnew"]

def main(argv=None):
  if argv is None:
    argv = sys.argv[1:]
  parser = argparse.ArgumentParser(
    description="Generate a model variant"
  )
  parser.add_argument("--RF", metavar="X", choices=CHOICES_RF, default=CHOICES_RF[0], help="choice of ConsRFna axiom: {0}".format(", ".join(CHOICES_RF)))
  parser.add_argument("--SC", metavar="X", choices=CHOICES_SC, default=CHOICES_SC[0], help="choice of SCReads axiom: {0}".format(", ".join(CHOICES_SC)))
  parser.add_argument("--RS", metavar="X", choices=CHOICES_RS, default=CHOICES_RS[0], help="choice of rseq definition: {0}".format(", ".join(CHOICES_RS)))
  parser.add_argument("--ST", metavar="X", choices=CHOICES_ST, default=CHOICES_ST[0], help="choice of sameThread definition: {0}".format(", ".join(CHOICES_ST)))
  parser.add_argument("--input", default="c11.cat-template", type=argparse.FileType('r'), help="Template cat file")
  parser.add_argument("--output", default="gen.cat", type=argparse.FileType('w'), help="Output cat file")
  parser.add_argument('herdflags', nargs='*', help="Passed to herd command-line")
  args = parser.parse_args(argv)
  if args.output.name == "stdout":
    args.output = sys.stdout
  choices = {
    "RF": args.RF,
    "SC": args.SC,
    "RS": args.RS,
    "ST": args.ST,
  }
  print("(* ({0}, {1}, {2}, {3}) *)".format(args.RF, args.SC, args.RS, args.ST), file=args.output)
  print("(* Autogenerated! Do not modify. *)", file=args.output)
  macro = None
  output = True
  for l in args.input:
    if l.startswith("#if") or l.startswith("#elif"):
      _unused1,key,_unused,val = l.split()
      assert key in choices.keys()
      output = val == choices[key]
      continue
    elif l.startswith("#endif"):
      output = True
      continue
    if output:
      print(l, file=args.output, end="")

  if args.output == sys.stdout or args.herdflags == []:
    return 0

  args.output.close()
  cmd = ['herd', '-conf', 'c11.cfg'] + args.herdflags
  print("model ({0}, {1}, {2}, {3}) generated in {4}".format(args.RF, args.SC, args.RS, args.ST, args.output.name))
  print(" ".join(cmd))
  return subprocess.call(cmd)

if __name__ == '__main__':
  sys.exit(main())
