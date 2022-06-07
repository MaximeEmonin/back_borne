package me.cocktail.utils;

import java.math.BigInteger;
import java.nio.ByteBuffer;
import java.util.Arrays;

public class BibData {
    public static int LENGTH = 16;

    private byte[] data;

    /* CONSTRUCTEUR 1 : encodage des données */
    public BibData(int quantity, int e_year, int e_month, int e_day, String type) {
        ByteBuffer bb = ByteBuffer.allocate(LENGTH);

        /* Quantité sur 2 octets */

        // quantity | 0xffff0000 :
        //  -> permet de s'assurer que le tableau sera de taille 4
        //  -> ne modifie pas les 2 premiers octets qui nous intéressent
        byte[] baQ = BigInteger.valueOf(quantity | 0xffff0000).toByteArray();
        bb.put(new byte[] {
                baQ[baQ.length - 2], baQ[baQ.length - 1]
        });

        /* Année sur 2 octets */

        // e_year | 0xffff0000 : idem
        byte[] baY = BigInteger.valueOf(e_year | 0xffff0000).toByteArray();
        bb.put(new byte[] {
                baY[baY.length - 2], baY[baY.length - 1]
        });

        /* Mois et Jour sur 1 octet chacun */
        bb.put((byte) (e_month & 0xff));
        bb.put((byte) (e_day & 0xff));

        /* Type sut les 10 octets restants */
        bb.put(type.getBytes());

        /* conversion du buffer en tableau de byte */
        data = bb.array();
    }

    /* CONSTRUCTEUR 2 : bytes */
    public BibData(byte[] bytes) {
        data = bytes;
    }

    /* Accesseur des bytes */
    public byte[] getBytes() {
        return data;
    }

    /* Méthodes de décodage */
    
    // & 0xff permet de récperer la valeur non signée lors de la conversion byte -> int
    public int getQuantity() {
        return ((data[0] & 0xff) << 8) | (data[1] & 0xff);
    }

    public int getExpirationYear() {
        return ((data[2] & 0xff) << 8) | (data[3] & 0xff);
    }

    public int getExpirationMonth() {
        return data[4] & 0xff;
    }

    public int getExpirationDay() {
        return data[5] & 0xff;
    }

    public String getType() {
        return new String(Arrays.copyOfRange(data, 6, 16));
    }
}
