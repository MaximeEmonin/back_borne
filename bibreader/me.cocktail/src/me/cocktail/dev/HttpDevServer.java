package me.cocktail.dev;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

import org.json.JSONException;
import org.json.JSONObject;

import me.cocktail.BibReader;
import me.cocktail.utils.Bib;
import me.cocktail.utils.BibData;
import me.cocktail.utils.BibID;

public class HttpDevServer implements HttpHandler {

    private BibReader reader;

    /*
     * Démarre la communication avec le lecteur qui sera utilisé lors des requêtes
     */
    public HttpDevServer() throws Exception {
        this.reader = new BibReader();
    }

    /*
     * Méthode de réponse aux requêtes
     * GET => retourne le tag ciblé, une erreur sinon
     * POST => ecrit le tag demandé, une erreur si le tag n'est pas ciblé
     */
    @Override
    public void handle(HttpExchange exchange) throws IOException {
        OutputStream os = exchange.getResponseBody();

        try {
            byte[] res;

            if ("POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                InputStream ios = exchange.getRequestBody();
                String data = new String(ios.readAllBytes());

                System.out.println(data);

                try {
                    JSONObject jsonData = new JSONObject(data);
                    JSONObject bibData = jsonData.getJSONObject("data");

                    Bib bib = new Bib(
                            new BibID(jsonData.getString("id")),
                            new BibData(
                                    bibData.getInt("quantity"),
                                    bibData.getInt("e_year"),
                                    bibData.getInt("e_month"),
                                    bibData.getInt("e_day"),
                                    bibData.getString("type")));

                    reader.writeTag(bib);
                    res = "OK\n".getBytes();
                } catch (JSONException e) {
                    throw new BibReader.BibReaderException("Bad data");
                }
            } else {
                JSONObject jsonRes = new JSONObject();
                Bib bib = reader.readTag();
                BibData bibData = bib.getData();

                JSONObject jsonResData = new JSONObject();
                jsonResData.put("quantity", bibData.getQuantity());
                jsonResData.put("e_year", bibData.getExpirationYear());
                jsonResData.put("e_month", bibData.getExpirationMonth());
                jsonResData.put("e_day", bibData.getExpirationDay());
                jsonResData.put("type", bibData.getType());

                jsonRes.put("id", bib.getID().getString());
                jsonRes.put("data", jsonResData);

                res = jsonRes.toString().getBytes();
            }
            exchange.sendResponseHeaders(HttpURLConnection.HTTP_OK, res.length);
            os.write(res);
            os.close();
        } catch (BibReader.BibReaderException e) {
            byte[] res = (e.getMessage() + "\n").getBytes();

            exchange.sendResponseHeaders(HttpURLConnection.HTTP_INTERNAL_ERROR, res.length);
            os.write(res);
            os.close();
        }
    }
}
