# Déploiement d’un Réseau de Neurones Profond sur Microcontrôleur

## 1. Analyse du modèle existant

Le modèle proposé est basé sur VGG11 mais adapté aux images 32×32 de CIFAR-10, avec une architecture progressive (32→64→128 filtres) qui réduit la taille à 16 Mo contre 528 Mo pour VGG11 classique. Il est composé de convolutions 3×3 avec ReLU, du Batch Normalization pour stabiliser l'entraînement, et une régularisation par SpatialDropout2D (0.25) dans les blocs convolutionnels et Dropout (0.3) dans les couches denses (1024→512→10 neurones). 

Nous avons testé ce modèle avant de commencer à le modifier, et nous atteignions 83% d'accuracy et 53% de loss. Ainsi, les performance de ce modèle sont correctes, et par la suite, nous essaierons de les concerver le mieux possibles tout en optimisant la taille de notre modèle.

---

## 2. Étude du microcontrôleur cible

Pour ce projet nous avions à notre disposition la carte STM32L4R9 Discovery Kit. Les principales caractéristiques à prendre en compte lors du choix de la carte sont la mémoire Flash, sur laquelle sera stocké le modèle, et la mémoire RAM qui effectuera les calculs du modèle.

Dans notre cas, la datasheet nous fournit les caractéristiques suivantes : une mémoire Flash de 2 Mo et une RAM de 640 Ko. La mémoire RAM devrait être suffisante, même si l'on risque d'observer plusieurs secondes d'inférence par image. Par contre, la Flash est insuffisante au vu de la taille actuelle de notre modèle (16 Mo). 

---

## 3. Évaluation de l’embarquabilité du modèle initial

Pour vérifier l'embarquabilité de notre modèle, nous avons créé un projet CubeIde pour notre carte, et analyser notre modèle avec STM32CubeAI. Voici les résultats obtenus :

![Analyse modèle de base](./img/first_analyse.png)

Comme prévu, la Flash est insuffisante pour contenir notre modèle.

---

## 4. Les solution pour rendre le modèle embarquable

### a. Compression du modèle

Une première solution pour rendre le modèle embarquable, est de le compresser. Ceci est directement possible avec STM32CubeAI, voici les résultats :

![Analyse modèle compressé](./img/compressed_model.png)

Après compression, la taille du modèle est siffisamment réduite pour pouvoir être stocké dans la Flash, le rendant ainsi embarquable.

### b. Création d'un modèle plus léger

La deuxième solution consiste à créer un tout nouveau modèle. Pour cela, nous avons modifié directement le fichier [train.py](./train.py) du modèle pour diminuer sa taille. 

---

## 5. Intégration dans un projet embarqué

La dernière étape du développement du projet consistait à intégrer notre modèle dans la carte. Pour cela, nous avons erécupéré notre nouveau fichier h5 et l'avons implémenté via CubeIde. Il faut ensuite entraîner le modèle directement sur la carte.

### a. Partie Python : envoi des datas vers la carte et évaluation

Le fichier [serial_evaluation.py](./serial_evaluation.py) gère la communication série entre notre PC et la carte : il synchronise l'UART, envoie des entrées (X_test) sous forme de floats 32, lit les sorties retournées par le STM32, compare les prédictions aux labels (Y_test) et calcule l'exactitude sur un nombre d'itérations donné.

Lors de nos premiers tests avec ce code, nous avons remarqué que nous ne recevions rien de la carte (*ValueError: attempt to get argmax of an empty sequence*). Nous avons donc rajouté un *time.sleep(5)* à la ligne 75 dans la fonction *evaluate_model_on_STM32*, après avoir envoyé les inputs, afin de laissé du temps de calcul à la carte. Ceci s'explique par la taille de la RAM du STM32L4R9, qui n'est pas assez importante pour réaliser les calculs aussi vite que sur notre ordinateur.

---

### b. Partie embarquée : réception des data et entrainement 

---

## 6. Évaluation des performances sur cible

---

## 7. Conclusion

---
