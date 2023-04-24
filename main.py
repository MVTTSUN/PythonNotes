from datetime import datetime
import os
import pyautogui

def writing_file(time, id, name, text):
  with open('./data.csv', 'a') as file:
    file.write(f'{time};{id};{name};{text}\n')

def full_writing_file(lines):
  with open('./data.csv', 'w') as file:
    for i in range(0, len(lines)):
      file.write(lines[i] + '\n')

def reading_file():
  with open('./data.csv', encoding='utf8') as file:
    return file.read().splitlines()

def read_note(line):
  print(f'''
    Номер заметки: {line[1]}
    Дата создания/редактирования: {line[0]}
    Название заметки: {line[2]}
    Текст заметки: {line[3]}

    -------------------------------------
  ''')

def show_notes(lines):
  print('Список заметок:')

  for i in range(0, len(lines)):
    line = lines[i].split(';')
    read_note(line)

def sort_notes(is_reverse):
  lines = reading_file()
  lines.sort(reverse=is_reverse)
  show_notes(lines)

is_work = True

if not os.stat('./data.csv').st_size == 0:
  lines = reading_file()
  id = int(lines[len(lines) - 1].split(';')[1])
else:
  id = 0

while is_work == True:
  command = input('Введите команду (к примеру help): ')

  if command == 'add':
    name = input('Введите название заметки: ')
    text = input('Введите текст заметки: ')
    id += 1
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    writing_file(time, id, name, text)

  if command.split(' ')[0] == 'delete':
    lines = reading_file()

    for i in range(0, len(lines)):
      line = lines[i].split(';')

      if line[1] == command.split(' ')[1]:
        lines.pop(int(command.split(' ')[1]) - 1)
        full_writing_file(lines)

  if command.split(' ')[0] == 'edit':
    lines = reading_file()

    for i in range(0, len(lines)):
      line = lines[i].split(';')

      if line[1] == command.split(' ')[1]:
        pyautogui.typewrite(line[2])
        name = input('Название заметки: ')
        pyautogui.typewrite(line[3])
        text = input('Текст заметки: ')
        id = line[1]
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        id_line = int(command.split(' ')[1]) - 1
        lines.pop(id_line)
        lines.insert(id_line, f'{time};{id};{name};{text}')
        full_writing_file(lines)
        break

  if command.split(' ')[0] == 'read':
    lines = reading_file()

    for i in range(0, len(lines)):
      line = lines[i].split(';')

      if line[1] == command.split(' ')[1]:
        read_note(line)

  if command == 'list':
    lines = reading_file()

    show_notes(lines)

  if command == 'list sort on date old':
    sort_notes(False)

  if command == 'list sort on date new':
    sort_notes(True)

  if command == 'exit':
    is_work = False

  if command == 'help':
    print('''
    add - добавить заметку
    delete {number notes} - удалить заметку
    edit {number notes} - отредактировать заметку
    read {number notes} - читать заметку
    list - посмотреть список заметок
    list sort on date old - сортировать заметки по дате от старых
    list sort on date new - сортировать заметки по дате от новых
    exit - выйти
    help - открыть список команд
    ''')