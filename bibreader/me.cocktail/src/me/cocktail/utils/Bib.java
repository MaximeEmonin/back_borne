package me.cocktail.utils;

public class Bib {
    private BibData data;
    private BibID id;

    public Bib(BibID bid, BibData bdata) {
        id = bid;
        data = bdata;
    }

    public BibData getData() {
        return data;
    }

    public BibID getID() {
        return id;
    }
}
