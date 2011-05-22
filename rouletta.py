#!/usr/bin/env python

import sys
import getopt

def einsatzkalkulator(guthaben, risikobereitschaft, guthabensicherheit):
  guthaben = guthaben - guthabensicherheit
  count = 0
  basis = 10

  while count < risikobereitschaft:
    count = 0
    einsatz = basis
    gesamteinsatz = 0

    while gesamteinsatz + einsatz <= guthaben:
      print einsatz
      gesamteinsatz = gesamteinsatz + einsatz
      einsatz = einsatz*2
      count = count+1

  
    print "Anzahl versuche: ", count
    print "Gesetzt insgesamt: ", gesamteinsatz
    print "---------------------"
    basis = basis - 0.01

  return basis + 0.01


def usage():
  print "einsatzkalkulator.py, version 0.1"
  print ""
  print "usage: einsatzkalulator.py [--help | -h]"
  print "                           [--credit <guthaben> | -c <guthaben> ]"
  print "                           [--risk <risikobereitschaft | -r <risikobereitschaft> ]"
  print "                           [--save <Restgeld> | -s <Restgeld>> ]"



def main(argv):
  # deklariere Variablen
  guthaben = 0
  risikobereitschaft = 0
  guthabensicherheit = 0

  # Optionen und Argumente parsen
  try:
    opts, args = getopt.getopt(argv, "hc:r:s:", ["help", "credit=", "risk=", "save="])
  except getopt.GetoptError as err:
    print(err)
    print ""
    usage()
    sys.exit(2)

  for opt, arg in opts:
    print opt + " " + arg
    if opt in ("-h", "--help"):
      usage()
      sys.exit()
    elif opt in ("-c", "--credit"):
      guthaben = float(arg)
    elif opt in ("-r", "--risk"):
      risikobereitschaft = float(arg)
    elif opt in ("-s", "--save"):
      guthabensicherheit = float(arg)

  # Wurde Guthaben nicht angegeben, so frage nach
  if guthaben == 0:
    guthaben = float(raw_input("Wie hoch ist dein Guthaben? "))

  # Wurde Risikobereitschaft nicht angegeben, so frage nach
  if risikobereitschaft == 0:
    risikobereitschaft = float(raw_input("Wie hoch ist deine Risikobereitschaft? "))

  # Endlosschleife
  while 1:
    gewinn = einsatzkalkulator(guthaben, risikobereitschaft, guthabensicherheit)

    guthaben = guthaben + gewinn
    frage = str(raw_input('Neues Guthaben? [' + str(guthaben) + '] '))
    if frage != "":
      guthaben = float(frage)


if __name__ == "__main__":
  main(sys.argv[1:])
