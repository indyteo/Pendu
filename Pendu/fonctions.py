# Gestion des possibilités du compte Admin

def procedure_Admin():
	import Pendu.donnees
	if saisir_mdp() == mdp("Admin"):
		import pickle
		verifier_score()
		with open('Pendu/scores', 'rb') as data:
			scores = pickle.Unpickler(data).load()
		print("\nLes scores sont :\n{}\n".format("\n".join(["-> {} = {}".format(joueur, score) for joueur, score in scores.items()])))
		
		#action = input("Quelle action voulez-vous effectuer ? ")
	else:
		print("Mot de passe incorrect !\n")

# Gestion du système de mot de passe

def saisir_mdp(): # Cette fonction demande au joueur de saisir le mot de passe.
	import tkinter # On importe le module graphique.
	fenetre = tkinter.Tk() # On crée une nouvelle fenêtre.
	tkinter.Label(tkinter.Frame(fenetre, width=200, borderwidth=10).pack(fill=tkinter.BOTH), text="Veuillez saisir le mot de passe :", fg="#0766ea").pack(fill=tkinter.BOTH) # On affiche les instructions.
	mdp = tkinter.StringVar() # On crée une variable qui nous premettra de récupérer la saisie du joueur.
	tkinter.Entry(fenetre, textvariable=mdp).pack(fill=tkinter.BOTH) # On crée une ligne de saisie pour que le joueur saisisse le mot de passe.
	tkinter.Button(fenetre, text="Valider", fg="green", bg="#c8f0c5", command=fenetre.quit).pack(fill=tkinter.BOTH) # On crée un bouton pour valider.
	fenetre.mainloop() # On attends que le joueur appuie sur "Valider" ou ferme la fenêtre.
	try: # On essaye,
		fenetre.destroy() # de supprimer la fenêtre.
	except: # Si il y a une erreur, autrement dit, si la fenêtre a été fermée par le joueur,
		pass # on passe.
	return mdp.get() # On renvoit le mot de passe saisit par le joueur.

def mdp(compte):
	import pickle
	with open('Pendu/mots_de_passe', 'rb') as data:
		mots_de_passe = pickle.Unpickler(data).load()
	return mots_de_passe[compte]

def securiser_compte():
	import pickle
	compte = input("Nom du compte à sécuriser : ")
	mdp = input("Nouveau mot de passe du compte : ")
	mdp_confirm = input("Répétez le mot de passe : ")
	if mdp == mdp_confirm:
		try:
			with open('Pendu/mots_de_passe', 'rb') as data:
				try:
					mots_de_passe = pickle.Unpickler(data).load()
				except:
					mots_de_passe = {}
		except FileNotFoundError:
			open('Pendu/mots_de_passe', 'w').close()
		mots_de_passe[compte] = mdp
		with open('Pendu/mots_de_passe', 'wb') as data2:
			pickle.Pickler(data2).dump(mots_de_passe)
		print("Le nouveau mot de passe du compte {} est désormais : {}.".format(compte, mdp))
	else:
		print("Les deux mots de passe ne correspondent pas !")
		securiser_compte()

# Gestion de la partie

def initialisation_partie(joueur): # Cette fonction est l'initialisation de "lancer_partie(joueur)".
	verifier_score(joueur) # On vérifie si le joueur a déjà un score ou non.
	from random import randrange # Pour choisir le mot aléatoirement.
	import Pendu.donnees # On récupère les données du fichier "donnees.py".
	mot = Pendu.donnees.mots[randrange(len(Pendu.donnees.mots))].lower() # On prend donc un mot aléatoirement venant du fichier "donnees.py".
	
	# /!\ A SUPPRIMER /!\ #
	
	#print("==> {} <==".format(mot).center(50)) # Pour les besoins de mes tests, on affiche le mot à découvrir.
	
	# /!\ A SUPPRIMER /!\ #
	
	c = list(mot) # On créé une liste nommée "c" dont les valeurs sont les lettres du mot, dans l'ordre.
	echecs_possibles = Pendu.donnees.chances # On récupère le nombre de chances, défini dans "donnees.py" également.
	print("Vous devez deviner le mot masqué avec {} échecs maximum.\n".format(echecs_possibles)) # On énonce les règles du jeu.
	for i, L in enumerate(mot): # On parcourt chaque caractère du mot,
		c[i] = "*" # puis on le masque.
	return mot, c, echecs_possibles # On renvoie les valeurs obtenues pour les récupérer dans la fonction principale.

def lancer_partie(joueur): # Le pseudo sera demandé au début.
	mot, c, echecs_possibles = initialisation_partie(joueur) # On réalise toutes les initialisations dans une fonction à part, pour plus de clarté.
	GG = x = False # Cette variable est vraie une fois qu'on a gagné. Elle permet d'arrêter le jeu à ce moment. "x" permet de savoir si on est au premier tour.
	while echecs_possibles != 0 and GG != True: # Tant qu'il nous reste des échecs possibles et qu'on a pas gagné.
		for i in c: # On parcourt chaque caractère de la liste,
			if echecs_possibles == 0: # Si le joueur a épuisé toutes ses chances,
				print("\nVous avez perdu !\nLe mot était : {}.\n".format(mot)) # on dit qu'il a perdu.
				return fin_partie(joueur, echecs_possibles) # On actualise le score du joueur et on le renvoie pour le récupérer dans le programme principal.
			if i == "*": # si il reste un ou plusieurs caractères masqués,
				if x == True: # si on est pas au premier tour,
					print("\nIl vous reste {} échecs possibles.\n".format(echecs_possibles)) # on affiche le nombre d'échecs possibles restant(s).
				else: # Sinon,
					x = True # on dit que le prochain tour ne sera plus le premier.
				print("Le mot est : {}.".format("".join(c))) # On affiche l'état de découverte du mot.
				GG, c, echecs_possibles = choix_joueur(mot, echecs_possibles, GG, c) # On traite le choix du joueur à part, pour plus de clarté.
				if GG == True: # Si le joueur a gagné,
					break # on sort de la boucle.
			else: # Sinon,
				if "".join("".join(c).split("*")) == "".join(c): # Si tous les caractères ont été découverts,
					print("\nVous avez gagné !\nLe mot était : {}.\n\nPoint(s) gagné(s) : {}.\n".format(mot, echecs_possibles)) # on dit au joueur qu'il a gagné.
					GG = True # On confirme qu'il a gagné.
					break # on sort de la boucle.
	return fin_partie(joueur, echecs_possibles) # On actualise le score du joueur et on le renvoie pour le récupérer dans le programme principal.

def choix_joueur(mot, echecs_possibles, GG, c): # Cette fonction est le traitement du choix du joueur de "lancer_partie(joueur)".
	OK = False # Cette variable est vraie une fois qu'on a vérifié le choix du joueur.
	while OK != True: # Tant qu'on a pas vérifié le choix du joueur,
		lettre = input("Votre choix : ").lower() # on demande au joueur de saisir sa lettre.
		if len(lettre) == 1 and lettre in "abcdefghijklmnopqrstuvwxyz": # Sinon, si le choix du joueur est bien une lettre,
			OK = True # on confirme qu'on a vérifié le choix du joueur.
		else: # Sinon,
			print("Rappel : Vous devez saisir une lettre, or vous avez saisit \"{}\" !".format(lettre)) # on remémore les règles au joueur.
	a = 0 # Cette variable est un compteur pour savoir si une lettre a été découverte ou non.
	for i, L in enumerate(mot): # On parcourt chaque lettre du mot,
		if L == lettre: # si une des lettres est le choix du joueur,
			c[i] = lettre # on la découvre dans le mot masqué.
			a += 1 # On augmente notre compteur car au moins une lettre a été découverte.
	if a == 0: # Si aucune lettre n'a été découverte,
		print("\nRaté !") # on dit au joueur qu'il s'est trompé.
		echecs_possibles -= 1 # On retire 1 au nombre d'échecs possibles.
	return GG, c, echecs_possibles # On renvoie les valeurs obtenues pour les récupérer dans la fonction principale.

def fin_partie(joueur, echecs_possibles): # Cette fonction est le traitement du score du joueur de "lancer_partie(joueur)".
	import pickle # On importe le module de traitement des fichiers.
	with open('Pendu/scores', 'rb') as data: # On ouvre le fichier des scores,
		scores = pickle.Unpickler(data).load() # et récupère les scores des joueurs.
	scores[joueur] += echecs_possibles # On actualise le score du joueur.
	with open('Pendu/scores', 'wb') as data2: # On rouvre le fichier des scores,
		pickle.Pickler(data2).dump(scores) # et on y place les scores.
	return scores[joueur] # On renvoie le score du joueur.

def menu_rejouer():
	import tkinter
	fenetre = tkinter.Tk()
	tkinter.Label(fenetre, text="Voulez-vous rejouer ?", fg="#0766ea").pack()
	tkinter.Button(fenetre, text="Oui", fg="green", bg="#c8f0c5", command=lambda *args: relancer_partie(fenetre, True)).pack(side="left")
	tkinter.Button(fenetre, text="Non", fg="red", bg="#f2c0c0", command=lambda *args: relancer_partie(fenetre, False)).pack(side="right")
	fenetre.mainloop()
	return rejouer

def relancer_partie(fenetre, relancer):
	import tkinter
	global rejouer
	rejouer = relancer
	fenetre.destroy()

# Gestion du score

def verifier_score(joueur="None"): # Cette fonction est la vérification du score du joueur de "initialisation_partie(joueur)".
	import pickle # On importe le module de traitement des fichiers.
	try: # On essaye,
		with open('Pendu/scores', 'rb') as data: # d'ouvrir le fichier des scores,
			scores = pickle.Unpickler(data).load() # et d'y récupérer les scores des joueurs.
	except FileNotFoundError: # Si le fichier n'existe pas,
		open('Pendu/scores', 'w').close() # on le crée.
	try: # On essaye,
		a = scores[joueur] # de récupérer le score du joueur en question.
	except NameError: # Si les scores n'existent pas,
		scores = {} # On les crée.
		with open('Pendu/scores', 'wb') as data2: # On ouvre le fichier des scores,
			pickle.Pickler(data2).dump(scores) # et on y place les scores.
	except KeyError: # Si le score du joueur n'existe pas,
		scores[joueur] = 0 # on le définit à 0.
		with open('Pendu/scores', 'wb') as data3: # On ouvre le fichier des scores,
			pickle.Pickler(data3).dump(scores) # et on y place les scores.

def afficher_score(joueur): # Cette fonction affiche le score d'un joueur.
	import pickle
	verifier_score(joueur) # On vérifie si le joueur a déjà un score ou non.
	with open('Pendu/scores', 'rb') as data: # On ouvre le fichier des scores,
		scores=pickle.Unpickler(data).load() # et récupère les scores des joueurs.
	return scores[joueur] # On renvoie le score du joueur.