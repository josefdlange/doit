# encoding: utf-8
import json
import os


class DataStore(object):
    data = None

    def __init__(self):
        self.data_dir = os.path.join(os.path.expanduser('~'), '.doit/')
        self.data_path = os.path.join(
            self.data_dir,
            'data.json'
        )
        self._setup()

    def _setup(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        try:
            with open(self.data_path, 'r') as f:
                self.data = json.load(f)
        except IOError, ValueError:
            self.data = []

    def save(self):
        with open(self.data_path, 'w+') as f:
            json.dump(self.data, f, indent=2)

    def add_task(self, task_text):
        new_task = {'text': task_text, 'state': 'pending'}
        self.data.append(new_task)
        self.save()
        return self.data.index(new_task)

    def complete_task(self, task_index):
        task = self.data[task_index]
        task['state'] = 'done'
        self.save()
        return self.data.index(task)

    def get_task(self, task_index):
        return self.data[task_index]

    def get_all_tasks(self):
        return self.data
    
    def get_done_tasks(self):
        returners = []
        for i, task in enumerate(self.data):
            if task.get('state') == 'done':
                returners.append((i, task))
        return returners

    def delete_task(self, index):
        self.data.pop(index)
        self.save()

    def delete_done_tasks(self):
        keepers = []
        for i, task in enumerate(self.data):
            if task.get('state') != 'done':
                keepers.append(task)
        self.data = keepers
        self.save()
