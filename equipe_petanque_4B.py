from csv import reader
from random import randint
from typing import Tuple, List
from time import perf_counter
import winsound

frequency = 800
duration = 500

liste_participant = []
TEMPS_ENTRE_2_ALGO = 120

# ouverture du fichier des participants et stockage dans une liste
with open("participant_petanque.csv", "r") as csv_file : 
	csv_reader = reader(csv_file)
		
	for line in csv_reader :
		liste_participant.append(line)
		
	csv_file.close()
	#-------------------------------------------------------------

#print(liste_participant)
#print(len(liste_participant)-1)

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



def comparaison_equipe_opti(lst_joueur_adversaire1 : List, lst_joueur_adversaire2 : List) :
	""".
	compare 2 listes et regarde si elles ont des tuples en commun
	>>> comparaison_equipe_opti([(2,7)],[(7,2)])
	True
	>>> comparaison_equipe_opti([(1,2,7)],[(2,7)])
	True
	>>> comparaison_equipe_opti([(1,2,7)],[(2,9,7)])
	True
	>>> comparaison_equipe_opti([(1,2,7)],[(2,9)])
	False
	"""
	for i in lst_joueur_adversaire1 :
		for j in lst_joueur_adversaire2 :
			compteur = 0
			# pas 2 fois dans une équipe de 3
			if len(i) == 5 and  len(j) >= 5 :
				for r in i[-3:] :
					for t in j[-3:] :
						if r == t :
							return True
			elif len(i) == 6 and  len(j) >= 5 :
				for y in i[-3:] :
					for w in j[-3:] :
						if y == w : return True
					for v in j[:3] :
						if y == v : return True
				for y in i[:3] :
					for w in j[-3:] :
						if y == w : return True
					for v in j[:3] :
						if y == v : return True
			# pas dans le même duel
			for k in i :
				for q in j :
					if q == k :
						compteur += 1
						if compteur == 2 :
							return True
	return False

def comparaison_equipe_degrade(lst_equipe1 : List, lst_equipe2 : List, lst_joueur_adversaire1 : List, lst_joueur_adversaire2 : List) :
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
	# pas dans la même équipe
	for i in lst_equipe1 :
		for j in lst_equipe2 :
			if i == j or i[::-1] == j:
				return True
			elif len(i) > 2 or len(j) > 2 :
				compteur = 0
				for k in i :
					for q in j :
						if q == k :
							compteur += 1
							if compteur == 2 :
								return True
	# pas contre le même adversaire et pas 2 fois dans une équipe de 3		
	for y in lst_joueur_adversaire1 :
		for v in lst_joueur_adversaire2 :
			if y[0] == v[0] :
				for w in y[1] :
					for x in v[1] :
						if w == x :
							return True
			if len(y[1]) == 3 and len(v[1]) == 3 :
				for r in y[1] :
					for t in v[1] :
						 if r == t : return True
									
	return False

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

		
if __name__ == "__main__":
	import doctest
	#doctest.testmod()
	tuple_nb_equipe = nb_equipe(len(liste_participant)-1)

	n=0#
	
	nb_parties = int(input("Combien de parties voulez vous (3 ou 4) ? "))
	while nb_parties != 3 and nb_parties != 4 :
		nb_parties = int(input("Combien de parties voulez vous (3 ou 4) ? "))

	temps_debut = perf_counter()
	# 1ère partie
	liste_equipe_t1 = creation_equipe(tuple_nb_equipe[0], tuple_nb_equipe[1])
	liste_duel_t1 = creation_liste_duel(liste_equipe_t1)
	liste_joueur_adversaire_t1 = creation_liste_joueur_adversaire(liste_equipe_t1)
	print(liste_duel_t1)
	
	print(f"\n{69* ' '}{13* '-'}\n{67* ' '} ! 1ère PARTIE ! \n{69* ' '}{13* '-'}\n")
	affichage_duel(liste_equipe_t1)
	
	# 2ème partie
	liste_equipe_t2 = creation_equipe(tuple_nb_equipe[0], tuple_nb_equipe[1])
	liste_duel_t2 = creation_liste_duel(liste_equipe_t2)
	liste_joueur_adversaire_t2 = creation_liste_joueur_adversaire(liste_equipe_t2)
	while (comparaison_equipe_opti(liste_duel_t1, liste_duel_t2)) and perf_counter() - temps_debut <= TEMPS_ENTRE_2_ALGO :
		liste_equipe_t2 = creation_equipe(tuple_nb_equipe[0], tuple_nb_equipe[1])
		liste_duel_t2 = creation_liste_duel(liste_equipe_t2)
		n+=1#

	if perf_counter() - temps_debut >= TEMPS_ENTRE_2_ALGO : # si le temps est écoulé
		liste_joueur_adversaire_t2 = creation_liste_joueur_adversaire(liste_equipe_t2)
		while comparaison_equipe_degrade(liste_equipe_t1, liste_equipe_t2, liste_joueur_adversaire_t1, liste_joueur_adversaire_t2) :
			liste_equipe_t2 = creation_equipe(tuple_nb_equipe[0], tuple_nb_equipe[1])
			liste_joueur_adversaire_t2 = creation_liste_joueur_adversaire(liste_equipe_t2)
			n+=1#
		
	print(f"\n{69* ' '}{13* '-'}\n{67* ' '} ! 2ème PARTIE ! \n{69* ' '}{13* '-'}\n")
	affichage_duel(liste_equipe_t2)
	winsound.Beep(frequency, duration)
	
	# 3ème partie
	liste_equipe_t3 = creation_equipe(tuple_nb_equipe[0], tuple_nb_equipe[1])
	liste_duel_t3 = creation_liste_duel(liste_equipe_t3)
	liste_joueur_adversaire_t3 = creation_liste_joueur_adversaire(liste_equipe_t3)
	while (comparaison_equipe_opti(liste_duel_t1, liste_duel_t3) or comparaison_equipe_opti(liste_duel_t2, liste_duel_t3)) and perf_counter() - temps_debut <= TEMPS_ENTRE_2_ALGO :
		liste_equipe_t3 = creation_equipe(tuple_nb_equipe[0], tuple_nb_equipe[1])
		liste_duel_t3 = creation_liste_duel(liste_equipe_t3)
		n+=1#
		
	if perf_counter() - temps_debut >= TEMPS_ENTRE_2_ALGO : # si le temps est écoulé
		liste_joueur_adversaire_t3 = creation_liste_joueur_adversaire(liste_equipe_t3)
		while comparaison_equipe_degrade(liste_equipe_t1, liste_equipe_t3, liste_joueur_adversaire_t1, liste_joueur_adversaire_t3) or comparaison_equipe_degrade(liste_equipe_t2, liste_equipe_t3, liste_joueur_adversaire_t2, liste_joueur_adversaire_t3) :
			liste_equipe_t3 = creation_equipe(tuple_nb_equipe[0], tuple_nb_equipe[1])
			liste_joueur_adversaire_t3 = creation_liste_joueur_adversaire(liste_equipe_t3)
			n+=1#
		
		
		
	print(f"\n{69* ' '}{13* '-'}\n{67* ' '} ! 3ème PARTIE ! \n{69* ' '}{13* '-'}\n")
	affichage_duel(liste_equipe_t3)
	winsound.Beep(frequency, duration)
	
	# 4ème partie
	if nb_parties == 4 :
		
		liste_equipe_t4 = creation_equipe(tuple_nb_equipe[0], tuple_nb_equipe[1])
		liste_duel_t4 = creation_liste_duel(liste_equipe_t4)
		liste_joueur_adversaire_t4 = creation_liste_joueur_adversaire(liste_equipe_t4)
		while (comparaison_equipe_opti(liste_duel_t1, liste_duel_t4) or comparaison_equipe_opti(liste_duel_t2, liste_duel_t4) or comparaison_equipe_opti(liste_duel_t3, liste_duel_t4)) and perf_counter() - temps_debut <= TEMPS_ENTRE_2_ALGO :
			liste_equipe_t4 = creation_equipe(tuple_nb_equipe[0], tuple_nb_equipe[1])
			liste_duel_t4 = creation_liste_duel(liste_equipe_t4)
			n+=1#
		r=0
		if perf_counter() - temps_debut >= TEMPS_ENTRE_2_ALGO : # si le temps est écoulé
			liste_joueur_adversaire_t4 = creation_liste_joueur_adversaire(liste_equipe_t4)
			while comparaison_equipe_degrade(liste_equipe_t1, liste_equipe_t4, liste_joueur_adversaire_t1, liste_joueur_adversaire_t4) or comparaison_equipe_degrade(liste_equipe_t2, liste_equipe_t4, liste_joueur_adversaire_t2, liste_joueur_adversaire_t4) or comparaison_equipe_degrade(liste_equipe_t3, liste_equipe_t4, liste_joueur_adversaire_t3, liste_joueur_adversaire_t4) :
				liste_equipe_t4 = creation_equipe(tuple_nb_equipe[0], tuple_nb_equipe[1])
				liste_joueur_adversaire_t4 = creation_liste_joueur_adversaire(liste_equipe_t4)
				n+=1#
				r+=1
				
		print(f"\n{69* ' '}{13* '-'}\n{67* ' '} ! 4ème PARTIE ! \n{69* ' '}{13* '-'}\n")
		affichage_duel(liste_equipe_t3)
		winsound.Beep(frequency, duration)
		
	print(n)
	if nb_parties == 4 :
		print(r)
	print(perf_counter() - temps_debut)

# made by Youenn AIGNELOT


