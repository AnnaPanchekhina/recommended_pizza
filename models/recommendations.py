from models.database import connect_to_db
import pandas as pd

class PizzaRecommender:
    def __init__(self):
        self.conn = connect_to_db()

    def recommend_by_age_gender(self, person_id):
        """Рекомендации на основе возраста и пола"""
        query = """
        SELECT pz.name, pz.rating, COUNT(pv.id) as visits
        FROM pizzeria pz
        JOIN person_visits pv ON pz.id = pv.pizzeria_id
        JOIN person p ON pv.person_id = p.id
        WHERE p.gender = (SELECT gender FROM person WHERE id = %s)
          AND p.age BETWEEN 
              (SELECT age - 5 FROM person WHERE id = %s) 
              AND 
              (SELECT age + 5 FROM person WHERE id = %s)
        GROUP BY pz.name, pz.rating
        ORDER BY visits DESC, pz.rating DESC
        LIMIT 3;
        """
        df = pd.read_sql(query, self.conn, params=(person_id, person_id, person_id))
        return df

    def recommend_by_city(self, person_id):
        """Рекомендации в том же городе"""
        query = """
        SELECT pz.name, pz.rating
        FROM pizzeria pz
        JOIN person_visits pv ON pz.id = pv.pizzeria_id
        JOIN person p ON pv.person_id = p.id
        WHERE p.address = (SELECT address FROM person WHERE id = %s)
        GROUP BY pz.name, pz.rating
        ORDER BY pz.rating DESC
        LIMIT 3;
        """
        df = pd.read_sql(query, self.conn, params=(person_id,))
        return df