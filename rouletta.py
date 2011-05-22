#!/usr/bin/env python

import sys
import getopt
from math import log


def usage():
  print "rouletta.py, version 0.1"
  print ""
  print "usage: rouletta.py [--help | -h]"
  print "                   [--credit <guthaben> | -c <guthaben> ]"
  print "                   [--risk <risikobereitschaft | -r <risikobereitschaft> ]"
  print "                   [--save <Restgeld> | -s <Restgeld> ]"
  print "                   [--min <Mindesteinsatz> ]"
  print "                   [--max <Maximaleinsatz> ]"
  print "                   [--segment <kleinste Stueckelung der Waehrung> ]"


def abrunden(zahl, schritt):
  return floor(zahl/schritt)*schritt


def main(argv):
  # deklariere Variablen
  guthaben = 0
  risikobereitschaft = 0
  guthabensicherheit = 0
  min = 0
  max = 0
  segment = 0

  # Optionen und Argumente parsen
  try:
    opts, args = getopt.getopt(argv, "hc:r:s:", ["help", "credit=", "risk=", "save=", "min=", "max=", "segment="])
  except getopt.GetoptError as err:
    print(err)
    print ""
    usage()
    sys.exit(2)

  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()
      sys.exit()
    elif opt in ("-c", "--credit"):
      guthaben = float(arg)
    elif opt in ("-r", "--risk"):
      risikobereitschaft = int(arg)
    elif opt in ("-s", "--save"):
      guthabensicherheit = float(arg)
    elif opt == "--min":
      min = float(arg)
    elif opt == "--max":
      max = float(arg)
    elif opt == "--segment":
      segment = float(arg)

  # Wurde Guthaben nicht angegeben
  if guthaben == 0:
    print "Guthaben fehlt."
    print ""
    usage()
    sys.exit(2)

  # Wurde Risikobereitschaft nicht angegeben
  if risikobereitschaft == 0:
    print "Risikobereitschaft fehlt."
    print ""
    usage()
    sys.exit(2)

  # Wurde Mindesteinsatz nicht angegeben
  if min == 0:
    print "Mindesteinsatz fehlt."
    print ""
    usage()
    sys.exit(2)

  # Wurde Maximaleinsatz nicht angegeben
  if max == 0:
    print "Maximaleinsatz fehlt."
    print ""
    usage()
    sys.exit(2)

  # Wurde Segment nicht angegeben
  if segment == 0:
    print "Die kleinste Stueckelung der Waehrung (Segment) fehlt."
    print ""
    usage()
    sys.exit(2)

  # Programm laeuft, solange Guthaben > 0 ist
  while guthaben > 0:
    # berechne Anzahl Stellen, auf die die Einsaetze gerundet werden sollen
    # damit mit der Stueckelung und den verfuegbaren Chips ein realistischer Einsatz moeglich ist
    stellen = int(round(log(segment , 10) * (-1)))

    # Berechne Einsatz-Grenze, so das beim letzten Zug das Tischlimit nicht ueberschritten wird
    grenze = round(float(max) / 2 ** (risikobereitschaft - 1), stellen)

    # berechne Einsatz anhand der Formel  e = (g - s) / (2^r - 1)
    # und runde das Ergebnis
    einsatz = round((guthaben - guthabensicherheit ) / (2 ** risikobereitschaft - 1), stellen)

    if einsatz < min:
      print "Setze Einsatz auf das Minimum, weil sonst das Tischlimit unterschritten wuerde"
      einsatz = min

    if einsatz > grenze:
      print "Drossle Einsatz, weil Tischlimit ueberschritten werden koennte"
      einsatz = grenze

    print "erster Einsatz: " + str(einsatz)
    print "letzter Einsatz: " + str(einsatz * 2 ** ( risikobereitschaft - 1 ))
    print "Nach " + str(int(risikobereitschaft)) + " verlorenen Spielen ausgegeben: " + str(einsatz * 2 ** risikobereitschaft - einsatz)

    guthaben = guthaben + einsatz
    try:
      frage = str(raw_input('Neues Guthaben? [' + str(guthaben) + '] '))
      if frage != "":
        guthaben = float(frage)
    except KeyboardInterrupt:
      # Guthaben wieder abzaehlen
      guthaben = guthaben - einsatz

      print ""
      print ""

      # Frage nach neuem Risikobereitschaft
      frage = str(raw_input('Neue Risikobereitschaft? [' + str(risikobereitschaft) + '] '))
      if frage != "":
        risikobereitschaft = int(frage)

      # Frage nach neuem Restgeld
      frage = str(raw_input('Neues Restgeld? [' + str(guthabensicherheit) + '] '))
      if frage != "":
        guthabensicherheit = float(frage)

      # Frage nach neuem Mindesteinsatz
      frage = str(raw_input('Neuer Mindesteinsatz? [' + str(min) + '] '))
      if frage != "":
        min = float(frage)

      # Frage nach neuem Maximaleinsatz
      frage = str(raw_input('Neuer Maximaleinsatz? [' + str(max) + '] '))
      if frage != "":
        max = float(frage)

      # Frage nach neuer Stueckelung
      frage = str(raw_input('Neue Stueckelung? [' + str(segment) + '] '))
      if frage != "":
        segment = float(frage)

    print 60 * "-"


if __name__ == "__main__":
  main(sys.argv[1:])
