from collections import OrderedDict
import sys
import os
from datetime import datetime

from peewee import *

db = SqliteDatabase('diary.db')

class Entry(Model):
  content = TextField()
  timestamp = DateTimeField(default = datetime.now)
  
  class Meta:
    database = db
    
    
    
def initialize():
  """Create the database if the don't exist."""
  db.connect()
  db.create_tables([Entry], safe=True)
  
def clear():
  os.system('cls' if os.name == 'nt' else 'clear')
    
    
def menu_loop():
  """Show the menu"""
  choice = None
  while choice != 'q':
    clear()
    print("Enter 'q to the quit'")
    for k,v in menu.items():
      print('{} {}'.format(k,v.__doc__))
    choice = input('Action:').lower().strip()
    
    if choice in menu:
      clear()
      menu[choice]()
      
      
  
  
def add_entry():
  """Add an Entry"""
  print('Enter your entry. Press "ctrl+d" when finished!')
  data = sys.stdin.read().strip()
  
  if data:
    if input('Save Entry [Y/N]').lower() != 'n':
      Entry.create(content=data)
      print("Saved Successfully")
  
  
  
def view_entry(search_query=None):
  """View Previous Entries"""
  entries = Entry.select().order_by(Entry.timestamp.desc())
  if search_query:
    entries = entries.where(Entry.content.contains(search_query))
  for entry in entries:
    timestamp = entry.timestamp.strftime('%A %B %d, %H:%M%p')
    time_str = "This Entry was made at:{}".format(timestamp)
    clear()
    print(time_str)
    print('=' * len(time_str))
    print(entry.content)
    print('\n\n'+'='*len(time_str))
    print('n) next entry')
    print('d) delete entry')
    print('q) return to the main menu')
    next_action = input('Action: [N\q]').lower().strip()
    if next_action == 'q':
      break
      
    elif next_action == 'd':
      delete_entry(entry)
      
def search_entry():
  """Search entries for a string."""
  view_entry(input('Search query: '))
  pass
  
    
def delete_entry(entry):
  """Delete an Entry"""
  if input('Are you sure? [y/n] ').lower() == 'y':
    entry.delete_instance()
    print('Entry deleted!')
  
menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entry),
    ('s', search_entry)
  ])
  
if __name__ == '__main__':
  initialize()
  menu_loop()
  