from Pendu.fonctions import *
joueur = "None"
while joueur == "None":
	joueur = input("Votre pseudo : ")
	if joueur == "None":
		print("Veuillez choisir un autre pseudo.\n")
	elif joueur == "Admin":
		procedure_Admin()
		joueur = "None"
	else:
		for i in joueur:
			if i.lower() not in "abcdefghijklmnopqrstuvwxyz_0123456789":
				print("Veuillez choisir un autre pseudo.")
				joueur = "None"
print("Votre score est de {}.".format(afficher_score(joueur)))
rejouer = True
while rejouer == True:
	input("\nAppuyer sur entrer pour lancer la partie.\n")
	print("Votre score est désormais de {}.".format(lancer_partie(joueur)))
	rejouer = menu_rejouer()