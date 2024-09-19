import json
from datetime import datetime

class Note:
    def __init__(self, id, title, body):
        self.id = id
        self.title = title
        self.body = body
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'timestamp': self.timestamp
        }

    @staticmethod
    def from_dict(data):
        note = Note(data['id'], data['title'], data['body'])
        note.timestamp = data['timestamp']
        return note


class NoteApp:
    def __init__(self, filename='notes.json'):
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            with open(self.filename, 'r') as file:
                notes_data = json.load(file)
                return [Note.from_dict(note) for note in notes_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_notes(self):
        with open(self.filename, 'w') as file:
            json.dump([note.to_dict() for note in self.notes], file, indent=4)

    def add_note(self, title, body):
        new_id = len(self.notes) + 1
        new_note = Note(new_id, title, body)
        self.notes.append(new_note)
        self.save_notes()

    def view_notes(self):
        for note in self.notes:
            print(f"ID: {note.id}, Title: {note.title}, Body: {note.body}, Date: {note.timestamp}")

    def edit_note(self, note_id, title, body):
        for note in self.notes:
            if note.id == note_id:
                note.title = title
                note.body = body
                note.timestamp = datetime.now().isoformat()
                break
        self.save_notes()

    def delete_note(self, note_id):
        self.notes = [note for note in self.notes if note.id != note_id]
        self.save_notes()


def main():
    app = NoteApp()

    while True:
        command = input("Введите команду (add, view, edit, delete, exit): ").strip().lower()
        
        if command == 'add':
            title = input("Введите заголовок: ")
            body = input("Введите тело заметки: ")
            app.add_note(title, body)
        elif command == 'view':
            app.view_notes()
        elif command == 'edit':
            note_id = int(input("Введите ID заметки для редактирования: "))
            title = input("Введите новый заголовок: ")
            body = input("Введите новое тело заметки: ")
            app.edit_note(note_id, title, body)
        elif command == 'delete':
            note_id = int(input("Введите ID заметки для удаления: "))
            app.delete_note(note_id)
        elif command == 'exit':
            break
        else:
            print("Неизвестная команда. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()