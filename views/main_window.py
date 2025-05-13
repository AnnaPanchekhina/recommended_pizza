from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget, QComboBox, QPushButton
from PySide6.QtCore import Qt
from models.recommendations import PizzaRecommender 

class MainWindow(QMainWindow):  
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pizza Recommendation System")
        self.setGeometry(100, 100, 600, 400)

        # Виджеты
        self.person_combo = QComboBox()
        self.recommend_button = QPushButton("Get Recommendations")
        self.result_label = QLabel("Recommendations will appear here")
        self.result_label.setAlignment(Qt.AlignTop)

        # Заполняем ComboBox пользователями
        self.load_persons()

        # Разметка
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select Person:"))
        layout.addWidget(self.person_combo)
        layout.addWidget(self.recommend_button)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Обработка кнопки
        self.recommend_button.clicked.connect(self.show_recommendations)

    def load_persons(self):
        """Загрузка списка пользователей из БД"""
        from models.database import connect_to_db
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM person;")
        persons = cursor.fetchall()
        for id, name in persons:
            self.person_combo.addItem(name, id)

    def show_recommendations(self):
        """Показ рекомендаций"""
        person_id = self.person_combo.currentData()
        recommender = PizzaRecommender()
        
        # Получаем рекомендации
        by_age_gender = recommender.recommend_by_age_gender(person_id)
        by_city = recommender.recommend_by_city(person_id)
        
        # Форматируем вывод
        text = "=== Recommendations ===\n"
        text += "\nBy Age & Gender:\n" + by_age_gender.to_string(index=False)
        text += "\n\nBy City:\n" + by_city.to_string(index=False)
        
        self.result_label.setText(text)