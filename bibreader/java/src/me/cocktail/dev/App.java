package me.cocktail.dev;

import java.net.InetSocketAddress;

import com.sun.net.httpserver.HttpServer;

public class App {
    /*
     * entrée de l'application
     * lance le serveur http de lecture/ecriture des tags
     */
    public static void main(String[] args) throws Exception {
        System.out.println("Starting bib tools...");

        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
        server.createContext("/api", new HttpDevServer());
        server.setExecutor(null);
        server.start();
    }
}
