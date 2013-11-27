SlideMaker
==========

Introduction
------------

Avec l'avènement du standard HTML5, de nombreuses options sont désormais offertes aux développeurs web, parmi lesquelles la création de présentations structurées en diapositives. Auparavant, ce type de présentation était le plus souvent réalisé avec Powerpoint ou des équivalents. Désormais, différents frameworks tels que Reveal permettent de réaliser des présentations intuitives, efficientes et élégantes.

Cependant, la préparation de telles présentations demande une bonne connaissance du langage HTML, et n'est pas toujours très aisée, notamment pour les éléments qui se répètent (titres de chapitres, pieds de pages, etc.). La mise au point d'un langage descriptif et d'un compilateur permettant de générer des slides HTML5 à partir de ce langage est proposée dans le cadre du cours "Compilateurs" dispensé au sein de la <a href="http://www.he-arc.ch">Haute Ecole Arc</a>

Objectifs
---------

Le langage et le compilateur créés devront permettre la réalisation de présentations HTML avec le framework Reveal. Les éléments suivants feront notamment partie du programme.

*	Langage structuré orienté objet ;
*	répartition des slides en groupes, avec titres de groupes ;
*	utilisation de "classes" prédéfinies pour générer les éléments "bas-niveaux" (listes à puces, paragraphes, titres, images) ;
*	utilisation de l'imbrication d'éléments pour la mise au point d'une présentation (une présentation contient des groupes, qui contiennent des slides, qui contiennent des éléments) ;
*	possibilité d'utiliser des layouts pour mettre en page le contenu des slides ;
*	possibilité d'utiliser une classe RichText pour générer des textes complexes comportant notamment différents styles (couleur, soulignement, etc.) ;
*	possibilité d'utiliser des boucles for pour générer des éléments de façon répétitive ;
*	possibilité d'ajouter des commentaires. 

Le langage doit permettre de décrire intégralement une présentation en déclarant des objets des différents types et en les imbriquant les uns dans les autres.

Le compilateur associé doit prendre en entrée un fichier écrit dans ce langage source, et fournir en sortie un fichier HTML fonctionnel, prêt à être intégré et lu dans le framework Reveal.

## Requis

* Python 3.3
* PLY 3.4 (Python Lex-Yacc)
* PyDot 1.0.3
* PyParsing 1.5.5
* Graphviz 2.3

## Documentation

* <a href="https://github.com/Chavjoh/SlideMaker/wiki">A propos du projet</a> 
* <a href="http://www.python.org/">A propos de python</a>
* <a href="http://www.dabeaz.com/ply/">A propos de PLY</a>
* <a href="https://code.google.com/p/pydot/">A propos de PyDot</a>
* <a href="http://pyparsing.wikispaces.com/">A propos de PyParsing</a>
* <a href="http://www.graphviz.org/">A propos de Graphviz</a>

Exemple
-------

L'exemple ci-dessous montre une ébauche du langage source défini au chapitre précédent, générant 6 slides dans un groupe, la première comportant un layout complexe pour afficher côte à côte une image et un paragraphe de texte, les suivantes étant générées dans une boucle pour afficher les images numérotée dans un dossier

```
Group("Titre de la section", "background: #00ff00")
{
	// Ceci est un commentaire
	Slide("background: #ff0000")
	{
		VerticalBox(20)
		{
			Title("20");
			HorizontalBox(20)
			{
				Image("image.png");
				List("unordered")
				{
					Text("Elément 1");
					RichText()
					{
						Element("Elé", "color: #ff0000");
						Element("ment ", "color: #00ff00, decoration: underline");
						Element("3", "color: #0000ff");
					}
					Text("Elément 3");
				}
			}
		}
	}

	/*
	 * Ceci est un commentaire sur plusieurs lignes
	 * Et ci-dessous une boucle génératrice de slides multiples
	 */
	For (i, 1, 5)
	{
		Slide()
		{
			Image("img" + i + ".png");
		}
	}
}

```
