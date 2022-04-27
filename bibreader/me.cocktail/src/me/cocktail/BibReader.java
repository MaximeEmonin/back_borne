package me.cocktail;

import java.util.Arrays;

import com.caen.RFIDLibrary.CAENRFIDException;
import com.caen.RFIDLibrary.CAENRFIDLogicalSource;
import com.caen.RFIDLibrary.CAENRFIDPort;
import com.caen.RFIDLibrary.CAENRFIDReader;
import com.caen.RFIDLibrary.CAENRFIDTag;

import me.cocktail.utils.Bib;
import me.cocktail.utils.BibData;
import me.cocktail.utils.BibID;

public class BibReader {
    private CAENRFIDLogicalSource source;

    /*
     * Démarre la communication avec le lecteur qui sera utilisé lors des requêtes
     */
    public BibReader() throws Exception {
        CAENRFIDReader reader = new CAENRFIDReader();

        try {
            reader.Connect(CAENRFIDPort.CAENRFID_RS232, "/dev/ttyS80");
        } catch (CAENRFIDException e) {
            throw new BibReaderException("Reader disconnected");
        }

        this.source = reader.GetSource("Source_0");
    }

    /*
     * détécte et retourne le tag ciblé sans le lire (sauf l'id)
     */
    private CAENRFIDTag getTag() throws BibReaderException {
        try {
            CAENRFIDTag[] Tags = this.source.InventoryTag();

            if (Tags == null)
                throw new BibReaderException("No tags");
            if (Tags.length != 1)
                throw new BibReaderException("Two many tags");

            return Tags[0];
        } catch (CAENRFIDException e) {
            throw new BibReaderException(e.getError());
        }
    }

    /*
     * lit le tag ciblé et retourne un objet JSON en bytes
     */
    public Bib readTag() throws BibReaderException {
        CAENRFIDTag tag = getTag();
        byte[] tagID = tag.GetId();

        try {
            byte[] data = this.source.ReadTagData_EPC_C1G2(
                    tag,
                    (short) 3,
                    (short) 0,
                    (short) 16);

            return new Bib(
                    new BibID(tagID),
                    new BibData(data));

        } catch (CAENRFIDException e) {
            throw new BibReaderException(e.getError());
        }
    }

    /*
     * vérifie que le tag démandé est ciblé
     * écrit le tag avec les nouvelle données
     */
    public void writeTag(Bib bib) throws BibReaderException {
        CAENRFIDTag tag = getTag();
        byte[] tagID = tag.GetId();

        if (!Arrays.equals(tagID, bib.getID().getBytes())) {
            throw new BibReaderException("Tag not available");
        }

        try {
            this.source.WriteTagData_EPC_C1G2(
                    tag,
                    (short) 3,
                    (short) 0,
                    (short) BibData.LENGTH,
                    bib.getData().getBytes());
        } catch (CAENRFIDException e) {
            throw new BibReaderException(e.getError());
        }
    }

    /*
     * classe d'exceptions internes
     */
    static public class BibReaderException extends Exception {
        public BibReaderException(String errorMessage) {
            super(errorMessage);
        }
    }
}
