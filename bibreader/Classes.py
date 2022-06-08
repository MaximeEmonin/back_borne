from jpype import startJVM, JClass

startJVM(classpath=["java/jar/me.cocktail.jar"])

# Classes
Bib = JClass("me.cocktail.utils.Bib")
BibID = JClass("me.cocktail.utils.BibID")
BibData = JClass("me.cocktail.utils.BibData")
BibReader = JClass("me.cocktail.BibReader")
BibReaderException = JClass("me.cocktail.BibReader.BibReaderException")
