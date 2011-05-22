#!/usr/bin/env python

import sys
import getopt
from math import log


def usage():
  print "name"
  print "     fuck the roulette"
  print "usage"
  print "     rouletta.py [--help | -h] <commands>"
  print ""
  print "commands"
  print "     -c, --credit <guthaben>"
  print "     -r, --risk <risikobereitschaft>"
  print "     --min <Mindesteinsatz>"
  print "     --max <Maximaleinsatz>"
  print "     --segment <kleinste Stueckelung der Waehrung>"


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

  # parse commands, options and arguments
  try:
    opts, args = getopt.getopt(argv, "hc:r:s:", ["help", "credit=", "risk=", "save=", "min=", "max=", "segment="])

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
  
    # if required commands are not given, raise a getopterror
    if guthaben == 0 or risikobereitschaft == 0 or min == 0 or max == 0 or segment == 0:
      raise getopt.GetoptError("the following commands are required: credit, risk, min, max, segment")
      sys.exit(2)
  
  # catch getopt errors
  except getopt.GetoptError as err:
    print "rouletta: " + str(err) + ". See './rouletta.py --help'"
    sys.exit(2)
  
  
  # program starts and runs unless credit > 0
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
