Гра **DuckHunt** на Python (бібліотека `pygame`)

## Запуск гри
1. Встановіть необхідні бібліотеки за допомогою pip:
   ```
   pip install -r requirements.txt
   ```
2. Запустіть файл `main.py`:
   ```
   python main.py
   ```

   
## Діаграми 

### Діаграма діяльності
Демонструє алгоритм ігрового циклу: рух качки, обробку пострілу, логіку "перемога/програш" та перехід між станами.
![Activity Diagram](https://github.com/AndreyShyshkin/DuckHunt/blob/master/docs/Activity%20Diagram.png)

### Діаграма класів
Показує об'єктно-орієнтовану структуру проєкту, включаючи основні класи (`Game`, `Driver`), механізм станів (`BaseState`, `PlayState`) та ігрові об'єкти (`Duck`, `Gun`).
![Class Diagram](https://github.com/AndreyShyshkin/DuckHunt/blob/master/docs/Class%20Diagram.png)

### Діаграма варіантів використання
Відображає взаємодію акторів (Гравця) з системою: налаштування гри, ігровий процес, стрільба та нарахування балів.
![Use Case Diagram](https://github.com/AndreyShyshkin/DuckHunt/blob/master/docs/Use%20Case%20Diagram.png)
