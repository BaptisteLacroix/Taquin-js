# M413 - TD2 : Réponses aux Questions

## Exercice	1 : Le	Jeux	de	Taquin (obligatoire)

Pour cet exercice vous devez partir de la page XHTML5 « taquin.html » et du fichier CSS
« css/taquin.css » fournis. Dans un premier temps, aucun ces deux éléments ne pourra être
modifié, seul le fichier JavaScript « taquin.js » le sera.
Vous trouverez le descriptif du Jeux de Taquin à l’URL suivante :
https://fr.wikipedia.org/wiki/Taquin
Bien lire l’ensemble des consignes avant de commencer à coder.
Pour cet exercice vous ne devrez pas utiliser les méthodes getElementByXY() et
getElementsByYZ() !
A vous de trouver d’autres solutions…
Complétez la fonction onLoad() qui ajoute de manière propre un écouteur sur l’évènement
« click » pour chaque élément HTML de type <div> étant dans le classe CSS « box ».

Ecrivez une fonction selection( event) qui échangera la position de la case vide avec la case sur
laquelle on vient de cliquer si et seulement si, ces deux cases ont un coté commun.
Pensez à utiliser l’objet JavaScript Math.
Vous n’avez pas le droit, pour le moment d’écrire d’autres fonctions.

````javascript
"use strict";

function onLoad() {
    console.log('Processus de chargement du document terminé…');
    let divs = document.getElementsByClassName('box');
    // Set a listener click on each divs
    for (let i = 0; i < divs.length; i++) {
        divs[i].addEventListener('click', function () {
            selection(divs[i]);
        });
    }
}

// Toute les ressources de la page sont complètement chargées.
window.onload = onLoad;


function selection(div) {
    let emptyBox = document.getElementsByClassName('empty')[0];
    let emptyBoxId = emptyBox.id;

    let emptyBoxIdX = emptyBoxId.split('-')[0][1];
    let emptyBoxIdY = emptyBoxId.split('-')[1][1];

    let boxId = div.id;
    let boxIdX = boxId.split('-')[0][1];
    let boxIdY = boxId.split('-')[1][1];

    if ((emptyBoxIdX === boxIdX && (Math.abs(boxIdY - emptyBoxIdY) === 1)) ||
        (emptyBoxIdY === boxIdY && (Math.abs(boxIdX - emptyBoxIdX) === 1))) {
        let temp = div.innerHTML;
        div.innerHTML = emptyBox.innerHTML;
        emptyBox.innerHTML = temp;

        // Set class .empty to the clicked box
        div.classList.add('empty');
        // And reove .empty from the empty box
        emptyBox.classList.remove('empty');
    }
}
````

- Que pouvez-vous dire de l'architecture de l'application ?

L'architecture de l'application est très simple, il y a une fonction qui est appelée au chargement de la page,
cette fonction ajoute un écouteur sur l'évènement click sur chaque élément HTML de type div qui a la classe CSS box.
Lorsque l'utilisateur clique sur un élément, la fonction selection est appelée avec l'élément cliqué en paramètre.
Cette fonction va vérifier si la case cliquée est adjacente à la case vide, si c'est le cas, les deux cases sont
échangées.

Pour exécuter le serveur, il faut installer python3 et pip3, puis lancer les commandes suivantes :

````bash
pip install Flask
pip install Flask-Cors
````

Ensuite, il faut lancer le serveur avec la commande suivante :

````bash
flask --app a_star.py run
````

Ensuite lancer le fichier index.html dans un navigateur web.
et le tour est joué.