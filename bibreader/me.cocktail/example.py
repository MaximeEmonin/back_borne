from jpype import startJVM, JClass

startJVM(classpath=["jar/me.cocktail.jar"])

# Classes
Bib = JClass("me.cocktail.utils.Bib")
BibID = JClass("me.cocktail.utils.BibID")
BibData = JClass("me.cocktail.utils.BibData")
BibReader = JClass("me.cocktail.BibReader")
BibReaderException = JClass("me.cocktail.BibReader.BibReaderException")
# ...

bibReader = BibReader()


while True:
    input('press enter to read...')
    try:
        tag = bibReader.readTag()
        tagId = tag.getID().getString()
        tagData = tag.getData()    
        print("ID :", tagId)
        print("Type :", tagData.getType())
        print("Quantité :", tagData.getQuantity())
        print("Péremption : {}/{}/{}".format(tagData.getExpirationDay(),tagData.getExpirationMonth(),tagData.getExpirationYear()))
   
    except BibReaderException as e:
        print("Erreur : ", e.getMessage())