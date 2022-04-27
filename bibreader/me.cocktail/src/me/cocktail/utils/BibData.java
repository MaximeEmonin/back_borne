package me.cocktail.utils;

import java.math.BigInteger;
import java.nio.ByteBuffer;
import java.util.Arrays;

public class BibData {
    public static int LENGTH = 16;

    private byte[] data;

    public BibData(int quantity, int e_year, int e_month, int e_day, String type) {
        ByteBuffer bb = ByteBuffer.allocate(LENGTH);

        byte[] baQ = BigInteger.valueOf(quantity | 0xffff0000).toByteArray();
        bb.put(new byte[] {
                baQ[baQ.length - 2], baQ[baQ.length - 1]
        });

        byte[] baY = BigInteger.valueOf(e_year | 0xffff0000).toByteArray();
        bb.put(new byte[] {
                baY[baY.length - 2], baY[baY.length - 1]
        });

        bb.put((byte) (e_month & 0xff));
        bb.put((byte) (e_day & 0xff));

        bb.put(type.getBytes());

        data = bb.array();
    }

    public BibData(byte[] bytes) {
        data = bytes;
    }

    /* Decode methods */
    public byte[] getBytes() {
        return data;
    }

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
