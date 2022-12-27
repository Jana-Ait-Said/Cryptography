# This Python file uses the following encoding: utf-8
import json

cle_publique = [143,7,103]
def chiffrer(lettre):
    """
        Chiffre une lettre avec la cryptographie RSA
        param :
                lettre (str) : la lettre
        return :
                lettre_final (int) : la lettre chiffrée
        """
    

    new_letter = ord(lettre)
    lettre_final = (new_letter**cle_publique[1])%cle_publique[0]
    return lettre_final

def completer(lettre,nbr):
    """
        Permet de coder la lettre d'un mot sur un nombre fixe de bits
        param :
                mot (int) : la lettre chiffrée
                nbr (int: le nombre de bits
        return :
                lettre(int): la lettre chiffrée sur un nombre nombre fixe de bits
        """
    
    l = len(lettre)
    if len(lettre)%nbr != 0:
        lettre = "0"*(nbr-l) + lettre
    return lettre

def Nbre_de_lettres(crypto):
    """
        Permet de determiner le nombre de lettres dans un mot 
        puisqu'une lettre est composée de 8 bits
        param :
                crypto (int) : le mot chiffré
        return :
                nbr_lettres (int): le nombre de lettres dans un mot 
        """

    l = len(crypto)
    completer_8 = 8
    debut = 0
    nbr_lettres = 0
    bits = crypto[0:completer_8]

    while bits != "00000000":
        nbr_lettres +=1
        debut += 8
        completer_8 += 8
        bits = crypto[debut:completer_8]
    return nbr_lettres
            

def chiffrer_mot(mot):
    """
        Chiffre un mot lettre par lettre en utilisant la cryptographie RSA
        en mettant chaque lettre sur un nombre fixe de bits et en effectuant une permutation
        param :
                mot(str) : le mot à chiffrer
        return :
                mot_final (int) : le mot chiffrée
        """


    listes_mot = []
    a = ""
    b = ""
    
    # Pour brouiller les pistes de décodages
    # A chaque lettre, selon les conditions ci-dessous, on atribut un 1,2 ou 3 en binaire
    # Cela permet aussi d'aider lors de la creation de ce projet
    # Car on peut visualiser plus facilement le nombre de lettre dans le mot
    # Mais à la fin on effectue une permuatation de sorte de ne pas faciliter le déchiffrement
    for i in mot:
        if chiffrer(i) < 10:
            listes_mot.append([ord(i)**(cle_publique[1])%cle_publique[0],format(1,"b")])
        elif chiffrer(i)  < 100 and chiffrer(i) >10 :
            listes_mot.append([ord(i)**(cle_publique[1])%cle_publique[0],format(2,"b")])
        elif chiffrer(i) >100 and chiffrer(i) < 1000:
            listes_mot.append([ord(i)**(cle_publique[1])%cle_publique[0],format(3,"b")])
   
    for n in range(len(listes_mot)):
        a+= completer(format(listes_mot[n][0],"b"),8)
        b  += format(listes_mot[n][1])
    mot = (a+8*"0"+ b)
    l = len(mot)
    mot_final = mot[(l//2):l]+ mot[0:(l//2)] # on effectue une permutation
    return mot_final

def dechiffrer_mot(crypto):
    """
        Déchiffre le mot  en défaisant la permutation,
        puis lorsque le nombre de lettres est trouvé,
        on défait le cryptage RSA lettre par lettre
        param :
                crypto(int) : le mot chiffrer
        return :
                mot_final (str) : le mot déchiffrée
        """

    cle_privee = [(cle_publique[2]),(cle_publique[0])]
    l = len(crypto)
    crypto = crypto[(l//2):l] + crypto[0:l//2] #on défait la permutation

    mot_dechiffrer = ""
    nbre_lettres = Nbre_de_lettres(crypto)
    debut_lettre = 0
    fin_lettre = 8

    # on met en format decimal lettre par lettre 
    #puis on defait la cryptographie RSA lettre par lettre
    # et on trouve la lettre correspondante dans la table ascii
    for i in range(nbre_lettres):
        mot = crypto[debut_lettre:fin_lettre]
        mot = int(mot,2)
        
        mot= (mot**cle_privee[0])%cle_privee[1]
        mot = chr(mot)
        mot_dechiffrer += mot
        debut_lettre += 8
        fin_lettre += 8
    return mot_dechiffrer


def acceder_bdd():
    """
        Permet d'afficher le contenu d'un fichier JSON comprenant 
        des clés lisibles auxquelles sont associées des mots de passe chiffrés 
        param :
                None
        return :
                None
        """

    json_data = None
    # On ouvre le fichier JSON en mode lecture
    with open('/Users/etudiant/Desktop/TLE-NSI/Crypto.json', 'r') as f:
        data = f.read()
    json_data = json.loads(data)
    print(json.dumps(json_data, indent = 4, sort_keys=True))

def rajouter_bdd(id,password):
    """
        Prend un identifiant et un mot de passe en paramètres, 
        et les rajoute dans le fichier JSON de la base de données.
        param :
                id (str): l'identifiant de l'utilisateur
                password(str): le mot de passe de l'utilisateur
        return :
                None
        """
    # On ouvre le fichier JSON en mode lecture
    jsonFile = open('/Users/etudiant/Desktop/TLE-NSI/Crypto.json', "r") 
    data = json.load(jsonFile)
    jsonFile.close() 

    ## On ajoute les données dans la mémoire
    data[id] = chiffrer_mot(password)

    ## On sauvegarde nos changements dans le fichier JSON 
    jsonFile = open('/Users/etudiant/Desktop/TLE-NSI/Crypto.json', "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()


def modifier_bdd(id,password):
    """
        Prend un identifiant et un mot de passe en paramètres, et modifie le contenu de
        l'entrée correspondant à identifiant dans le fichier JSON de la base de données
        param :
                id (str): l'identifiant de l'utilisateur
                password(str): le mot de passe de l'utilisateur
        return :
                None
    """
    # On ouvre le fichier JSON en mode lecture
    jsonFile = open('/Users/etudiant/Desktop/TLE-NSI/Crypto.json', "r") 
    data = json.load(jsonFile) 
    jsonFile.close() 

    ## On modifie les données dans la mémoire
    tmp = data[id] 
    data[id] = chiffrer_mot(password)

    ## On sauvegarde nos changements dans le fichier JSON 
    jsonFile = open('/Users/etudiant/Desktop/TLE-NSI/Crypto.json', "w+")
    jsonFile.write(json.dumps(data))

def access_portal(id,password):
    """
        Prend un identifiant et un mot de passe en paramètres et vérifie que le mot
        de passe entré correspondant au mot de passe chiffré de l'utilisateur
        dans le fichier JSON de la base de données
        Si c'est le cas on affiche "ACESS AUTORISÉ" sinon "ACESS REFUSÉ"
        param :
                id (str): l'identifiant de l'utilisateur
                password(str): le mot de passe de l'utilisateur
        return :
                None
        """
    # On ouvre le fichier JSON en mode lecture
    with open('/Users/etudiant/Desktop/TLE-NSI/Crypto.json',"r") as fichier:
        data = json.load(fichier)
    if data[id]== chiffrer_mot(password):
        print("ACESS AUTORISÉ")
    else:
        print("ACESS REFUSÉ")


