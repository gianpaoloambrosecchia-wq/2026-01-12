from database.DB_connect import DBConnect
from model.Constructor import Constructor
from model.arco import Arco


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(anno1, anno2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)

        # RICORDA!!
        # - is not null per verificare che un campo non sia nullo
        # - nomeTabella.* per prendere tutti i dati di una sola tabella (se faccio il join tra piu tabelle)
        query = """select distinct c.*
                    from constructors c, results re, races ra
                    where c.constructorId = re.constructorId and re.raceId = ra.raceId and re.position is not null
                    and ra.year >= %s and ra.year <= %s
                    """

        cursor.execute(query, (anno1, anno2))

        for row in cursor:
            results.append(Constructor(**row))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getAllEdges(idMap, anno1, anno2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)

        # Vuole i piloti che per lo stesso costruttore hanno partecpiato a gare diverse: considero due
        # tabelle per races, constructors e results perche mi servono due costruttori e piloti che hanno
        # partecipato a gare diverse (due races diverse).
        query = """SELECT c1.constructorId as c1, c2.constructorId as c2, COUNT(DISTINCT re1.driverId) AS peso
                    FROM constructors c1, constructors c2, 
                         results re1, results re2, 
                         races ra1, races ra2
                    WHERE c1.constructorId = re1.constructorId
                      AND c2.constructorId = re2.constructorId
                      AND re1.driverId = re2.driverId
                      AND c1.constructorId < c2.constructorId
                      AND re1.raceId = ra1.raceId
                      AND re2.raceId = ra2.raceId
                      AND ra1.raceId != ra2.raceId
                      AND re1.position IS NOT NULL
                      AND re2.position IS NOT NULL
                      AND ra1.year >= %s and ra1.year <= %s
                      AND ra2.year >= %s and ra2.year <= %s
                    GROUP BY c1.constructorId, c2.constructorId
                    """

        # RICORDA di passare tutti i parametri che ti servono nell'ordine in cui li inserisci nella query
        cursor.execute(query, (anno1, anno2, anno1, anno2))

        for row in cursor:
            results.append(Arco(idMap[row["c1"]], idMap[row["c2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results

