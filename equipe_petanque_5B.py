from csv import reader
from random import randint
from typing import Tuple, List
from time import perf_counter 
import winsound

frequency = 800
duration = 500

liste_participant = []
TEMPS_ENTRE_2_ALGO = 60

# ouverture du fichier des participants et stockage dans une liste
with open("participant_petanque.csv", "r") as csv_file : 
	csv_reader = reader(csv_file)
		
	for line in csv_reader :
		liste_participant.append(line)
		
	csv_file.close()
	#-------------------------------------------------------------
	

def nb_equipe(nb_participant : int) -> Tuple :
	"""
	calcule le nombre de duo et trio nécessaire
	>>> nb_equipe(8)
	(4, 0)
	>>> nb_equipe(9)
	(3, 1)
	>>> nb_equipe(10)
	(2, 2)
	>>> nb_equipe(11)
	(1, 3)
	>>> nb_equipe(12)
	(6, 0)
	"""
	nb_trio = nb_participant % 4
	nb_duo = nb_participant // 4 * 2 - nb_trio
	return nb_duo , nb_trio

def creation_equipe(nb_duo : int, nb_trio : int) :
	"""
	crée des tuples de 2 ou 3, qui determine l'index des participants en équipe
	"""
	assert (nb_duo + nb_trio) % 2 == 0 and (nb_duo + nb_trio) != 0
	num = list(range(1, nb_duo*2 + nb_trio*3 +1, 1))# liste tout les nombres de 1 jusqu'au nombre de participants
	equipe = []
	
	for i in range(nb_duo) : # crée les tuples des duo
		num1 = num[randint(0, len(num)-1)]
		num.remove(num1)
		num2 = num[randint(0, len(num)-1)]
		num.remove(num2)
		equipe.append((num1, num2))
		
	for j in range(nb_trio) : # crée les tuples des trio
		num1 = num[randint(0, len(num)-1)]
		num.remove(num1)
		num2 = num[randint(0, len(num)-1)]
		num.remove(num2)
		num3 = num[randint(0, len(num)-1)]
		num.remove(num3)
		equipe.append((num1, num2, num3))
		
	return equipe

def comparaison_equipe_opti(partie_1 : List, partie_2 : List, liste_j_equipe_3) :
	""".
	compare 2 listes et regarde si elles ont des tuples en commun
	retourn False si les listes sont bonnes
	>>> comparaison_equipe_opti([(2,7)],[(7,2)])
	True
	>>> comparaison_equipe_opti([(1,2,7)],[(2,7)])
	True
	>>> comparaison_equipe_opti([(1,2,7)],[(2,9,7)])
	True
	>>> comparaison_equipe_opti([(1,2,7)],[(2,9)])
	False
	"""
	# vérifie pas 2 fois dans une équipe de 3
	for equipe1 in partie_1 :				
		if len(equipe1) == 3 :
			for j3 in liste_j_equipe_3 :
				for joueur1 in equipe1 :
					if j3 == joueur1 :
						return True
	#--------------------------------------
			
	# vérifie pas dans le même duel
	lst_duel_1 = creation_liste_duel(partie_1)
	lst_duel_2 = creation_liste_duel(partie_2)
			
	for duel1 in lst_duel_1 :
		for duel2 in lst_duel_2 :
			compteur = 0
			
			for k in duel1 :
				for q in duel2 :
					if q == k :
						compteur += 1
						if compteur == 2 :
							return True
	#------------------------------
	return False

def comparaison_equipe_degrade(partie_1 : List, partie_2 : List, liste_j_equipe_3 : List) :
	""".
	compare 2 listes et regarde si elles ont des tuples en commun
	>>> comparaison_equipe([(2,7)],[(7,2)])
	True
	>>> comparaison_equipe([(1,2,7)],[(2,7)])
	True
	>>> comparaison_equipe([(1,2,7)],[(2,9,7)])
	True
	>>> comparaison_equipe([(1,2,7)],[(2,9)])
	False
	"""
	# vérifie pas 2 fois dans la même équipe
	for equipe1 in partie_1 :
		for equipe2 in partie_2 :
			if equipe1 == equipe2 or equipe1[::-1] == equipe2:
				return True
			elif len(equipe1) > 2 or len(equipe2) > 2 :
				cmt = 0
				for joueur1 in equipe1 :
					for joueur2 in equipe2 :
						if joueur1 == joueur2 :
							cmt += 1
							if cmt == 2 :
								return True
	#-----------------------------------

	# vérifie pas 2 fois contre le même adversaire
	lst_joueur_adversaire1 = creation_liste_joueur_adversaire(partie_1)
	lst_joueur_adversaire2 = creation_liste_joueur_adversaire(partie_2)
	for j_a1 in lst_joueur_adversaire1 :
		for j_a2 in lst_joueur_adversaire2 :
			if j_a1[0] == j_a2[0] :
				for adversaire1 in j_a1[1] :
					for adversaire2 in j_a2[1] :
						if adversaire1 == adversaire2 :
							return True
	# --------------------------------------------
	
	# vérifie pas 2 fois dans une équipe de 3
	for equipe1 in partie_1 :				
		if len(equipe1) == 3 :
			for j3 in liste_j_equipe_3 :
				for joueur1 in equipe1 :
					if j3 == joueur1 :
						return True
	#--------------------------------------
									
	return False

def comparaison_equipe_degrade_plus(partie_1 : List, partie_2 : List, liste_j_equipe_3 : List) :
	""".
	compare 2 listes et regarde si elles ont des tuples en commun
	>>> comparaison_equipe([(2,7)],[(7,2)])
	True
	>>> comparaison_equipe([(1,2,7)],[(2,7)])
	True
	>>> comparaison_equipe([(1,2,7)],[(2,9,7)])
	True
	>>> comparaison_equipe([(1,2,7)],[(2,9)])
	False
	"""
	# vérifie pas 2 fois dans la même équipe
	for equipe1 in partie_1 :
		for equipe2 in partie_2 :
			if equipe1 == equipe2 or equipe1[::-1] == equipe2:
				return True
			elif len(equipe1) > 2 or len(equipe2) > 2 :
				cmt = 0
				for joueur1 in equipe1 :
					for joueur2 in equipe2 :
						if joueur1 == joueur2 :
							cmt += 1
							if cmt == 2 :
								return True
	#-----------------------------------

	# vérifie pas 2 fois contre le même adversaire
	lst_joueur_adversaire1 = creation_liste_joueur_adversaire(partie_1)
	lst_joueur_adversaire2 = creation_liste_joueur_adversaire(partie_2)
	for j_a1 in lst_joueur_adversaire1 :
		for j_a2 in lst_joueur_adversaire2 :
			if j_a1[0] == j_a2[0] :
				for adversaire1 in j_a1[1] :
					for adversaire2 in j_a2[1] :
						if adversaire1 == adversaire2 :
							return True
	# --------------------------------------------
									
	return False

def creation_liste_joueur_equipe_de_3(lst : List, lst_a_trie : List) -> List :

	for equipe in lst_a_trie :
		if len(equipe) == 3 :
			lst.append(equipe[0])
			lst.append(equipe[1])
			lst.append(equipe[2])

	return lst
	
def creation_liste_duel(equipe : List) :
	joueur_adversaire = []
	for i in range(0, len(equipe), 2) :
		if len(equipe[0+i]) == 3 :
			joueur_adversaire.append((equipe[0+i][0], equipe[0+i][1], equipe[0+i][2], equipe[1+i][0], equipe[1+i][1], equipe[1+i][2]))
			
		elif len(equipe[1+i]) == 3 :
			joueur_adversaire.append((equipe[0+i][0], equipe[0+i][1], equipe[1+i][0], equipe[1+i][1], equipe[1+i][2]))

		else :
			joueur_adversaire.append((equipe[0+i][0], equipe[0+i][1], equipe[1+i][0], equipe[1+i][1]))
			
	return joueur_adversaire

def creation_liste_joueur_adversaire(equipe : List) :
	joueur_adversaire = []
	for i in range(0, len(equipe), 2) :
		if len(equipe[0+i]) == 3 :
			joueur_adversaire.append((equipe[0+i][0], (equipe[1+i][0], equipe[1+i][1], equipe[1+i][2])))
			joueur_adversaire.append((equipe[0+i][1], (equipe[1+i][0], equipe[1+i][1], equipe[1+i][2])))
			joueur_adversaire.append((equipe[0+i][2], (equipe[1+i][0], equipe[1+i][1], equipe[1+i][2])))
			joueur_adversaire.append((equipe[1+i][0], (equipe[0+i][0], equipe[0+i][1], equipe[0+i][2])))
			joueur_adversaire.append((equipe[1+i][1], (equipe[0+i][0], equipe[0+i][1], equipe[0+i][2])))
			joueur_adversaire.append((equipe[1+i][2], (equipe[0+i][0], equipe[0+i][1], equipe[0+i][2])))
			
		elif len(equipe[1+i]) == 3 :
			joueur_adversaire.append((equipe[0+i][0], (equipe[1+i][0], equipe[1+i][1], equipe[1+i][2])))
			joueur_adversaire.append((equipe[0+i][1], (equipe[1+i][0], equipe[1+i][1], equipe[1+i][2])))
			joueur_adversaire.append((equipe[1+i][0], (equipe[0+i][0], equipe[0+i][1])))
			joueur_adversaire.append((equipe[1+i][1], (equipe[0+i][0], equipe[0+i][1])))
			joueur_adversaire.append((equipe[1+i][2], (equipe[0+i][0], equipe[0+i][1])))
			
		else :
			joueur_adversaire.append((equipe[0+i][0], (equipe[1+i][0], equipe[1+i][1])))
			joueur_adversaire.append((equipe[0+i][1], (equipe[1+i][0], equipe[1+i][1])))
			joueur_adversaire.append((equipe[1+i][0], (equipe[0+i][0], equipe[0+i][1])))
			joueur_adversaire.append((equipe[1+i][1], (equipe[0+i][0], equipe[0+i][1])))
	
	return joueur_adversaire

def affichage_duel(equipe : List) :
	"""
	affiche les equipes qui vont s'affronter avec le nom et prenom des menmbres des equipes
	"""
	assert len(equipe)%2 == 0 and len(equipe) != 0
	for i in range(0, len(equipe), 2) :
		nb_espace = 70 - len(str(f"{liste_participant[equipe[0+i][0]][0]} / {liste_participant[equipe[0+i][1]][0]} / {liste_participant[equipe[0+i][2]][0]}" if len(equipe[0+i]) == 3 else f"{liste_participant[equipe[0+i][0]][0]} / {liste_participant[equipe[0+i][1]][0]}")) #nb d'espace pour centrer le mot contre
		
		if len(equipe[0+i]) == 3 :
			print(f"{liste_participant[equipe[0+i][0]][0]} / {liste_participant[equipe[0+i][1]][0]} / {liste_participant[equipe[0+i][2]][0]} {nb_espace * ' '} contre {10* ' '} {liste_participant[equipe[1+i][0]][0]} / {liste_participant[equipe[1+i][1]][0]} / {liste_participant[equipe[1+i][2]][0]}")
		
		elif len(equipe[1+i]) == 3 :
			print(f"{liste_participant[equipe[0+i][0]][0]} / {liste_participant[equipe[0+i][1]][0]} {nb_espace * ' '} contre {10* ' '} {liste_participant[equipe[1+i][0]][0]} / {liste_participant[equipe[1+i][1]][0]} / {liste_participant[equipe[1+i][2]][0]}")
			
		else :
			print(f"{liste_participant[equipe[0+i][0]][0]} / {liste_participant[equipe[0+i][1]][0]} {nb_espace * ' '} contre {10* ' '} {liste_participant[equipe[1+i][0]][0]} / {liste_participant[equipe[1+i][1]][0]} ")

		print(f"\n{160*'-'} \n")

def verif_tt_comparaison(liste_equipe_prec : List, liste_equipe, liste_j_equipe_3, type_verif : str):
	"""

	"""
	if  type_verif == "opti" :
		for equipe_prec in liste_equipe_prec :
			if comparaison_equipe_opti(liste_equipe, equipe_prec, liste_j_equipe_3) :
				return True

	elif type_verif == "dégradé" :
		for equipe_prec in liste_equipe_prec :
			if comparaison_equipe_degrade(liste_equipe, equipe_prec, liste_j_equipe_3) :
				return True

	elif type_verif == "dégradé +" :
		for equipe_prec in liste_equipe_prec :
			if comparaison_equipe_degrade_plus(liste_equipe, equipe_prec, liste_j_equipe_3) :
				return True
				
	return False
	
def creation_affichage_partie(tmp_debut : float, num_partie : int, nb_equipe : Tuple, liste_equipe_prec : List, liste_j_equipe_3 : List, n : int) :
	"""

	"""
	if TEMPS_ENTRE_2_ALGO > perf_counter() - tmp_debut :
		type_verif = "opti"
		liste_equipe = creation_equipe(nb_equipe[0], nb_equipe[1])
		while perf_counter() - tmp_debut <= TEMPS_ENTRE_2_ALGO and verif_tt_comparaison(liste_equipe_prec, liste_equipe, liste_j_equipe_3, type_verif):
			liste_equipe = creation_equipe(nb_equipe[0], nb_equipe[1])
			n += 1

	if 2*TEMPS_ENTRE_2_ALGO > perf_counter() - tmp_debut >= TEMPS_ENTRE_2_ALGO  : # si le 1er temps est écoulé
		type_verif = "dégradé"
		liste_equipe = creation_equipe(nb_equipe[0], nb_equipe[1])
		while 2*TEMPS_ENTRE_2_ALGO > perf_counter() - tmp_debut >= TEMPS_ENTRE_2_ALGO and verif_tt_comparaison(liste_equipe_prec, liste_equipe, liste_j_equipe_3, type_verif):
			liste_equipe = creation_equipe(nb_equipe[0], nb_equipe[1])
			n += 1

	if perf_counter() - tmp_debut >= 2*TEMPS_ENTRE_2_ALGO  : # si le 2eme temps est écoulé
		type_verif = "dégradé +"
		liste_equipe = creation_equipe(nb_equipe[0], nb_equipe[1])
		while perf_counter() - tmp_debut >= 2*TEMPS_ENTRE_2_ALGO and verif_tt_comparaison(liste_equipe_prec, liste_equipe, liste_j_equipe_3, type_verif):
			liste_equipe = creation_equipe(nb_equipe[0], nb_equipe[1])
			n += 1
			
	if num_partie == 1 :
		apres_num_partie = "ère"
	else :
		apres_num_partie = "ème"
		
	print(f"\n{69* ' '}{13* '-'}\n{67* ' '} ! {num_partie}{apres_num_partie} PARTIE ! {type_verif}\n{69* ' '}{13* '-'}\n")
	affichage_duel(liste_equipe)
	winsound.Beep(frequency, duration)
	
	return n,liste_equipe

if __name__ == "__main__":
	#import doctest
	#doctest.testmod()
	tuple_nb_equipe = nb_equipe(len(liste_participant)-1)
	liste_equipes_precedentes = []
	nb_test = 0
	num_partie = 0
	liste_j_equipe_3 = []
	
	print(f"Nombre de participant : {len(liste_participant)-1}\n")
	
	nb_parties = int(input("Combien de parties voulez vous ? "))
	
	temps_debut = perf_counter()
	
	for i in range(nb_parties) :
		num_partie += 1
		nb_test, liste_equipe = creation_affichage_partie(temps_debut , num_partie, tuple_nb_equipe, liste_equipes_precedentes, liste_j_equipe_3, nb_test)
		liste_equipes_precedentes.append(liste_equipe)
		liste_j_equipe_3 = creation_liste_joueur_equipe_de_3(liste_j_equipe_3, liste_equipe)
	
	
	print(f"nombre de tentatives : {nb_test}")
	print(f"temps d'éxecution : {int(perf_counter() - temps_debut)}s\n")
	for i in liste_equipes_precedentes:
		print(i)
	
	
# made by Youenn AIGNELOT


