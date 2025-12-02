from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio

class DAO:

    @staticmethod
    def get_connessione() -> dict[str, Connessione] | None:

        cnx = DBConnect.get_connection()
        result = {}

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM connessione"
        try:
            cursor.execute(query)
            for row in cursor:
                connessione = Connessione(
                    id=row["id"],
                    id_rifugio1=row["id_rifugio1"],
                    id_rifugio2=row["id_rifugio2"],
                    distanza=row["distanza"],
                    difficolta=row["difficolta"],
                    durata=row["durata"],
                    anno=row["anno"]
                )
                result[connessione.id] = connessione
        except Exception as e:
            print(f"Errore durante la query get_connesione: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def get_rifugio() -> dict[str, Rifugio] | None:

        cnx = DBConnect.get_connection()
        result = {}

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM rifugio"
        try:
            cursor.execute(query)
            for row in cursor:
                rifugio = Rifugio(
                    id=row["id"],
                    nome=row["nome"],
                    localita=row["localita"],
                    altitudine=row["altitudine"],
                    capienza=row["capienza"],
                    aperto=row["aperto"]
                )
                result[rifugio.id] = rifugio
        except Exception as e:
            print(f"Errore durante la query get_rifugio: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result
