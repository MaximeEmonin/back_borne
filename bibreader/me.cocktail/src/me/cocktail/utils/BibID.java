package me.cocktail.utils;

import java.util.Base64;

public class BibID {
    private byte[] id;

    public BibID(String s) {
        id = Base64.getDecoder().decode(s);
    }

    public BibID(byte[] ba) {
        id = ba;
    }

    /* decode methods */
    public byte[] getBytes() {
        return id;
    }

    public String getString() {
        return new String(Base64.getEncoder().encode(id));
    }
}
