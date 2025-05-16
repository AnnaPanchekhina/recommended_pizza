from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QComboBox, 
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel
)
from PySide6.QtCore import Qt
from models.database import connect_to_db

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pizza Recommendation System")
        self.setGeometry(100, 100, 800, 600)

        # Виджеты
        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            "По имени", 
            "По возрасту", 
            "По пиццерии", 
            "По минимальному рейтингу", 
            "По названию пиццы"
        ])
        
        self.value_input = QLineEdit(placeholderText="Введите значение...")
        self.search_button = QPushButton("Поиск")
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(6)  # Колонки: Имя, Возраст, Пиццерия, Рейтинг, Пицца, Цена
        
        # Разметка
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Критерий поиска:"))
        layout.addWidget(self.filter_combo)
        layout.addWidget(self.value_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Обработка кнопки
        self.search_button.clicked.connect(self.search_data)

    def search_data(self):
        """Поиск данных по выбранному критерию"""
        filter_type = self.filter_combo.currentText()
        value = self.value_input.text().strip()
        
        if not value:
            return

        query = ""
        if filter_type == "По имени":
            query = f"""
            SELECT p.name, p.age, pz.name, pz.rating, m.pizza_name, m.price
            FROM person p
            JOIN person_visits pv ON p.id = pv.person_id
            JOIN pizzeria pz ON pv.pizzeria_id = pz.id
            JOIN menu m ON pz.id = m.pizzeria_id
            WHERE p.name ILIKE '%{value}%'
            """
        elif filter_type == "По возрасту":
            query = f"""
            SELECT p.name, p.age, pz.name, pz.rating, m.pizza_name, m.price
            FROM person p
            JOIN person_visits pv ON p.id = pv.person_id
            JOIN pizzeria pz ON pv.pizzeria_id = pz.id
            JOIN menu m ON pz.id = m.pizzeria_id
            WHERE p.age = {int(value)}
            """
        elif filter_type == "По пиццерии":
            query = f"""
            SELECT p.name, p.age, pz.name, pz.rating, m.pizza_name, m.price
            FROM person p
            JOIN person_visits pv ON p.id = pv.person_id
            JOIN pizzeria pz ON pv.pizzeria_id = pz.id
            JOIN menu m ON pz.id = m.pizzeria_id
            WHERE pz.name ILIKE '%{value}%'
            """
        elif filter_type == "По минимальному рейтингу":
            query = f"""
            SELECT p.name, p.age, pz.name, pz.rating, m.pizza_name, m.price
            FROM person p
            JOIN person_visits pv ON p.id = pv.person_id
            JOIN pizzeria pz ON pv.pizzeria_id = pz.id
            JOIN menu m ON pz.id = m.pizzeria_id
            WHERE pz.rating >= {float(value)}
            """
        elif filter_type == "По названию пиццы":
            query = f"""
            SELECT p.name, p.age, pz.name, pz.rating, m.pizza_name, m.price
            FROM person p
            JOIN person_visits pv ON p.id = pv.person_id
            JOIN pizzeria pz ON pv.pizzeria_id = pz.id
            JOIN menu m ON pz.id = m.pizzeria_id
            WHERE m.pizza_name ILIKE '%{value}%'
            """

        self.run_query(query)

    def run_query(self, query):
        """Выполняет SQL-запрос и выводит результат в таблицу"""
        conn = connect_to_db()
        if not conn:
            return

        cursor = conn.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # Настройка таблицы
            self.result_table.setRowCount(len(rows))
            self.result_table.setHorizontalHeaderLabels([
                "Имя", "Возраст", "Пиццерия", "Рейтинг", "Пицца", "Цена"
            ])
            
            # Заполнение данными
            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.result_table.setItem(row_idx, col_idx, item)
                    
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            conn.close()