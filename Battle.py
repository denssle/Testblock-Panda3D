# -*- coding: utf-8 -*-

import Items,random
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject


def werteBerechnen(spieler):
    """Berechnet temporaer fuer den Kampf den Angriffs- und Verteidigungswert aus den Attributen des Spielers und seines Equipments"""
    spieler.angriff += spieler.waffe.wert
    spieler.verteidigung += spieler.ruestung.wert + spieler.hose.wert + spieler.schuhe.wert + spieler.helm.wert
    return spieler

def Angriff(angreifer,verteidiger):
    """Schadensberechnung bei Angriff, eventuell weicht der Verteidiger aus. Kritische Treffer m�glich, die die Geschicklichkeit verringern"""
    ausweichen = verteidiger.geschicklichkeit - angreifer.geschicklichkeit
    if ausweichen <= 0:
        ausweichen = 0                              # Ausweichwahrscheinlichkeit
    if random.randint(1,100) > ausweichen:
        schaden = angreifer.angriff - verteidiger.verteidigung + random.randint(0,angreifer.angriff)    # Schadensberechnung
        if schaden <= 0:
            schaden = 1
        krit = angreifer.angriff-verteidiger.verteidigung
        if verteidiger.energie < (verteidiger.maxenergie / 3):
            krit += 10
            if krit > 100:
                krit = 100
        if random.randint(1,100) < krit:
            if verteidiger.geschicklichkeit / 5 < 1:            # Kritischer Treffer Berechnung
                abzug = 1
            else:
                abzug = verteidiger.geschicklichkeit / 5
            verteidiger.geschicklichkeit -= abzug
            if verteidiger.geschicklichkeit <= 0:
                verteidiger.geschicklichkeit = 1
            print "Kritischer Treffer"
    else:
        print "Ausgewichen!"
        schaden = 0
    return schaden
        
        
def ItemUse(item,spieler):
    """ Prueft den Typ des uebergebenen Items und fuehrt dann ja nach Typ eine Aktion aus. Muss noch mit allen Itemtypen erweitert werden"""
    if item.typ == "Energie":
        spieler.energie += item.wert
        if spieler.energie > spieler.maxenergie:
            spieler.energie = spieler.maxenergie
    elif item.typ == "Mana":
        spieler.mana += item.wert
        if spieler.mana > spieler.maxmana:
            spieler.mana = spieler.maxmana
    else:
        print "Item bisher nicht benutzbar"

def eventhandleGegner(spieler,gegner):
    """Laesst den Gegner eine Aktion ausfuehren"""
    schaden = Angriff(gegner,spieler)
    spieler.energie -= schaden
    if spieler.energie < 0:
            spieler.energie = 0
    
def eventhandleSpieler(aktion,spieler,gegner,aktNr,pos):
    """Laesst den Spieler eine Aktion ausfuehren"""
    if aktion == "angriff":
        schaden = Angriff(spieler,gegner)
        gegner.energie -= schaden
        if gegner.energie < 0:
            gegner.energie = 0
    elif aktion == "item":
        item = spieler.inventar.getItem(aktNr,pos)
        if item <> None:
            ItemUse(item,spieler)
            spieler.inventar.entfernen(aktNr,pos)
        
            
def anzeigen(spieler,gegner):
    """ Zeigt Energie von Gegner und Spieler an, erstmal provisorisch"""
    print "Kampf: \n%s \t Energie: %i" %(spieler.name,spieler.energie)
    print "%s \t Energie: %i Geschick: %i" %(gegner.name,gegner.energie,gegner.geschicklichkeit)

def setKey(self, key, value):
        self.keyMap[key] = value

def Kampf(spieler,gegner):
    """Startet einen Kampf zwischen Spieler und Gegner, bis einer der beiden keine Energie mehr hat
    Usereingaben sind moeglich wie Item oder Angriff"""
    aktion = "angriff"
    aktNr = 0
    pos = [0,0]
    keyhandler = DirectObject()
    keyMap = {"angriff":0,"item":0}
    spieler = werteBerechnen(spieler)
    
    DirectObject.accept(keyhandler,"a", setKey, ["angriff",1])
    DirectObject.accept(keyhandler,"i", setKey, ["item",1])
    
    if (keyMap["angriff"]!=0):
        aktion = angriff
    if (keyMap["item"]!=0):
        aktion = item
    if spieler.energie <= 0:
        print "Spieler tot"
        return [spieler,gegner,False]
    elif gegner.energie <= 0:
        print "Gegner besiegt"
        return [spieler,gegner,False]        
    print "Spieler greift an"
    eventhandleSpieler(aktion,spieler,gegner,aktNr,pos)
    aktion = "angriff"
    print "Gegner greift an"
    eventhandleGegner(spieler,gegner)
    anzeigen(spieler,gegner)
    return [spieler,gegner,True]
