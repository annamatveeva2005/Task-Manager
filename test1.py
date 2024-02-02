import json
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from colorama import Fore as F
import argparse


class TaskStatus(Enum):# Определение перечисления TaskStatus, представляющего возможные статусы задач
    new = 'новая'
    in_progress = 'выполняется'
    review = 'ревью'
    done = 'выполнено'
    cancelled = 'отменено'


@dataclass
class Task:
    name: str
    description: str
    status: TaskStatus
    date: datetime
    status_history: list = field(default_factory=list)
    statuses = [
        TaskStatus.cancelled,
        TaskStatus.new,
        TaskStatus.in_progress,
        TaskStatus.review,
        TaskStatus.done
    ]

    def change_status_increase(self):  # Определение метода для повышения статуса задачи
        now_status = self.status
        index_now_status = self.statuses.index(now_status)
        if index_now_status < len(self.statuses) - 1:
            self.status = self.statuses[index_now_status + 1]
        else:
            print(f"[ ✅ ] Задача '{self.name}' уже сделана")

    def change_status_reduction(self):  # Определение метода для уменьшения статуса задачи
        now_status = self.status
        index_now_status = self.statuses.index(now_status)
        if index_now_status > 0:
            self.status = self.statuses[index_now_status - 1]
        else:
            print(f"[ ✅ ] Задача '{self.name}' уже отменена")

    def change_status_cancel(self):  # Определение метода для отмены статуса задачи
        now_status = self.status
        index_now_status = self.statuses.index(now_status)
        if index_now_status > 0:
            self.status = TaskStatus.cancelled
        else:
            print(f"[ ✅ ] Задача '{self.name}' уже отменена")


@dataclass
class TaskManager:  # Определение класса TaskManager, управляющего списком задач
    filename: str
    tasks: list[Task] = field(default_factory=list)
    view: list = field(default_factory=list)

    def add_task(self, name, description, status, date):  # Метод для добавления новой задачи
        task = Task(
            name,
            description,
            {status.value: status for status in TaskStatus}.get(status),
            datetime.strptime(date, "%Y-%m-%d")
        )
        self.tasks.append(task)

        self.write_tasks()  # сохранение

    def write_tasks(self):  # Метод для записи задач в файл
        with open(self.filename, 'w', encoding="utf-8") as file:
            data = []
            for task in self.tasks:
                task_dct = {
                    "name": task.name,
                    "description": task.description,
                    "status": task.status.value,
                    "date": task.date.strftime("%Y-%m-%d"),  # перевод даты в строку
                    "status_history": [date_.strftime("%Y-%m-%d") for date_ in task.status_history]
                    # перевод каждой даты в строки
                }
                data.append(task_dct)
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load_tasks(self):  # Метод для загрузки задач из файла
        try:
            with open(self.filename, 'r', encoding="utf-8") as file:
                data = json.load(file)
                self.tasks = []
                for task in data:
                    task = Task(
                        name=task["name"],
                        description=task["description"],
                        status=TaskStatus(task["status"]),
                        date=datetime.strptime(task["date"], "%Y-%m-%d"),
                        status_history=[datetime.strptime(date_, "%Y-%m-%d") for date_ in task["status_history"]]
                    )
                    self.tasks.append(task)
        except Exception as e:
            pass

    def view_tasks(self):  # Метод для просмотра списка задач
        for index, task in enumerate(self.tasks, 1):
            result = f"[ {F.LIGHTCYAN_EX}{index}{F.RESET} ] {F.MAGENTA}{task.name} ({task.description}){F.RESET} ⇒ {F.YELLOW}{task.status.value}{F.RESET}"
            print(result)

    def change_task_status(self, task_index, flag):  # Метод для изменения статуса задачи
        task = self.tasks[task_index - 1]
        task.status_history.append(datetime.now().date())

        if flag == "1":
            task.change_status_increase()
        elif flag == "2":
            task.change_status_reduction()
        elif flag == "3":
            task.change_status_cancel()

        self.write_tasks()

    def delete_all_tasks(self):  # Метод для удаления всех задач из списка
        self.tasks = []
        self.write_tasks()

    def __post_init__(self):  # при каждом запуске срабатывает "магический" метод, он подгружает данные
        self.load_tasks()


parser = argparse.ArgumentParser(description='Парсер')
parser.add_argument('filename', help='название файла')

args = parser.parse_args()

task_manager = TaskManager(args.filename)

method = input(
    f"{F.MAGENTA}Выберите действие:\n "
    f"{F.YELLOW}1. Добавить новую задачу\n "
    f"2. Посмотреть список задач\n "
    f"3. Изменить статус задачи\n "
    f"4. Удалить все задачи\n{F.RESET}")
if method == '1':
    name_of_task = input(f"{F.MAGENTA}Введите название задачи:{F.RESET}\n")
    description_of_task = input(f"{F.MAGENTA}Введите описание задачи:{F.RESET}\n")
    status_of_task = input(
        f"{F.MAGENTA}Введите статус задачи {F.YELLOW}(новая/выполняется/ревью/выполнено/отменено){F.MAGENTA}:{F.RESET}\n")
    date_of_task = input(f"{F.MAGENTA}Введите дату создания задачи {F.YELLOW}(год-месяц-день){F.MAGENTA}:{F.RESET}\n")
    task_manager.add_task(name_of_task, description_of_task, status_of_task, date_of_task)
elif method == '2':
    task_manager.view_tasks()
elif method == '3':
    index_of_task = int(input(f"{F.MAGENTA}Введите номер задачи {F.YELLOW}(начиная с единицы){F.MAGENTA}:{F.RESET}\n"))
    flag_of_task = input(f"{F.MAGENTA}Выберите действие\n"
                         f"{F.YELLOW}1. Повысить статус \n"
                         f"2. понизить статус \n"
                         f"3. отменить задачу{F.MAGENTA}{F.RESET}\n")
    task_manager.change_task_status(index_of_task, flag_of_task)
elif method == '4':
    task_manager.delete_all_tasks()
    print(f"{F.YELLOW}Все задачи удалены{F.RESET}")
