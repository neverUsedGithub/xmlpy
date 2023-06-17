from xmlpy import transpile_file
import sys
import os

rargs = sys.argv[1:]

def printUsage():
  print("""Usage: python cli.py <file>
-o, --output <file>  : output file
-f, --factory <name> : the element factory
-h, --help           : show this help menu
-n, --no-header      : don't write the xmlpy header""")

if len(rargs) == 0:
  printUsage()
  exit(1)

no_header = False
output = None
indx = 0
xmlpy_factory = None

args = []
while indx < len(rargs):
  arg = rargs[indx]
  if arg.startswith("-"):
    if arg == "-h" or arg == "--help":
      printUsage()
      exit(0)
    elif arg == "-o" or arg == "--output":
      if indx + 1 >= len(rargs):
        printUsage()
        exit(1)
      indx += 1
      output = rargs[indx]
    elif arg == "-n" or arg == "--no-header":
      no_header = True
    elif arg == "-f" or arg == "--factory":
      if indx + 1 >= len(rargs):
        printUsage()
        exit(1)
      indx += 1
      xmlpy_factory = rargs[indx]
  else:
    args.append(arg)
  indx += 1

if len(args) == 0:
  printUsage()
  print("Missing input file.")
  exit(1)

filepath = os.path.abspath(args[0])
if not os.path.exists(filepath) or not os.path.isfile(filepath):
  printUsage()
  print(f"'{filepath}' is not a file.")
  exit(1)

content = transpile_file(
  filepath,
  add_header=not no_header,
  xmlpy_factory=xmlpy_factory
)
outputfile = None

if output is not None:
  outputfile = os.path.abspath(output)
else:
  outputfile = os.path.join(
    os.path.dirname(filepath),
    os.path.splitext(os.path.basename(filepath))[0] + ".py"
  )

with open(outputfile, "w") as f:
  f.write(content)