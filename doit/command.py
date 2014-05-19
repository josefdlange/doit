# encoding: utf-8
from random import choice
import textwrap

import clint
from clint.textui import colored, indent, puts

from storage import DataStore

INDENT = 2
INDENT_LARGE = 4


class Command(object):

    def __init__(self, *args, **kwargs):
        self.storage = DataStore()

    def _app_string(self):
        return colored.cyan('DoIt!')

    def overview(self):
        return self.show(None, None)

    def show(self, major, minor):
        tasks = self.storage.get_all_tasks()
        pending_tasks = []
        done_tasks = []
        for i, task in enumerate(tasks):
            if task.get('state') == 'done':
                done_tasks.append((i, task))
            else:
                pending_tasks.append((i, task))
        with indent(INDENT):
            if len(pending_tasks) > 0:
                puts('Here\'s what you still need to do:')
                with indent(INDENT):
                    for task in pending_tasks:
                        puts('({}): {}'.format(task[0], task[1].get('text')))
                if len(done_tasks) > 0:
                    puts('\n\n')
            if len(done_tasks) > 0:
                puts ('Here\'s what you\'ve accomplished so far:')
                with indent(INDENT):
                    for task in done_tasks:
                        puts('({}): {}'.format(task[0], task[1].get('text')))

    def add(self, major, minor):
        new_task_index = self.storage.add_task(major)
        with indent(INDENT):
            puts('Got it. You need to {}. This has been assigned #{}.'.format(major[0].lower() + major[1:], new_task_index))

    def finish(self, task_number):
        index = self.storage.complete_task(int(task_number))
        task = self.storage.get_task(index)
        with indent(INDENT):
            puts('Awesome! You\'re done with {}. High-five!'.format(task.get('text')[0].lower() + task.get('text')[1:]))

    def delete(self, task_number):
        task = self.storage.get_task(int(task_number))
        response = raw_input('Are you sure you want to delete "({}): {}"? Y/N: '.format(task_number, task.get('text')))
        if response.lower().startswith('y'):
            self.storage.delete_task(int(task_number))
            with indent(INDENT):
                puts('Alright, looks like you won\'t {}{}"'.format(task.get('text')[0].lower(), task.get('text')[1:]))

    def flush(self):
        self.storage.delete_done_tasks()
        with indent(INDENT):
            puts("Nice. Totally cleaned up your done tasks.")

    def done(self):
        tasks = self.storage.get_done_tasks()
        with indent(INDENT):
            for task in tasks:
                puts('({}): {}'.format(task[0], task[1].get('text')))

    def execute(self):
        args = clint.Args()
        command = args.get(0)
        major = args.get(1)
        minor = args.get(2)
        if not command:
            return self.overview()
        self.delegate(command, major, minor)

    def delegate(self, command, major, minor):
        if command == 'show':
            return self.show(major, minor)
        elif command == 'help' or command[0] == '-':
            return self.help()
        elif command == 'add':
            return self.add(major, minor)
        elif command == 'finish':
            return self.finish(major)
        elif command == 'done':
            return self.done()
        elif command == 'flush':
            return self.flush()
        elif command == 'delete':
            return self.delete(major)

    def empty(self):
        text = '''
            You have no tasks. You can add some like this:
              $ doit add "Write a sweet to-do list"
            Show your tasks with:
              $ doit show
                You have 1 task!
                (1) Write a sweet to-do list
            Complete it like this:
              $ doit finish 1
                Are you sure you want to finish "Write a sweet to-do list"? (Y/N) Y
                Done. "Write a sweet to-do list" is finished.
            '''
        print textwrap.dedent(text)

    def help(self):
        text = '''
            ==== DoIt : Help =============================================

            doit                        show all of your tasks
            doit show                   also show all of your tasks
            doit help                   show this help message

            doit add <text>             create a new task with the text
            doit finish <taskno>        finish task with that number
            doit delete <taskno>        delete task with that number

            doit done                   show finished tasks
            doit flush                  delete all finished tasks

            ==============================================================
            '''
        with indent(INDENT):
            puts(textwrap.dedent(text))


def main():
    Command().execute()


if __name__ == '__main__':
    main()
