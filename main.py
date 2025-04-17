import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import re
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

window = Tk()
window.title('Spotify Repeat Rewind')
playlist_link = StringVar()
viable_link = False
playlist_id = ''
load_dotenv()

scope = "user-library-read, user-top-read, playlist-modify-private, playlist-modify-public, playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def regex_input(*event):
  input = playlist_link.get()
  if 'https://open.spotify.com/playlist/' in input:
    button_fill['state'] = NORMAL
    set_playlist_id(input)
  elif button_fill['state'] == NORMAL:
    button_fill['state'] = DISABLED

def set_playlist_id(input):
  global playlist_id
  regex = re.compile(r"t\/(.+?)\?", re.MULTILINE)
  playlist_id = regex.search(input).groups()[0]

def process_playlist():
  global playlist_id, button_fill
  results = sp.current_user_top_tracks(limit=20, offset=0, time_range='short_term')
  playlist_items = [i['id'] for i in results['items']]
  if playlist_id:
    sp.playlist_replace_items(playlist_id=playlist_id, items=playlist_items)
  messagebox.showinfo(title='Playlist Built', message='Added songs to playlist.')
  button_fill['state'] = DISABLED

def build_main():
  global button_fill
  window.rowconfigure(0, minsize=800, weight=1)
  window.columnconfigure(0, minsize=800, weight=1)

  field_frame = Frame(window, relief=FLAT)
  button_fill = Button(field_frame, text="Fill Playlist", command=process_playlist, state=DISABLED)
  label_playlist = Label(field_frame, text='Playlist URL')
  field_playlist = Entry(field_frame, textvariable=playlist_link, width=96)

  playlist_link.trace_add('write', regex_input)

  label_playlist.grid(row=0, column=0, padx=5, pady=5)
  field_playlist.grid(row=0, column=1, padx=5, pady=5)
  button_fill.grid(row=1, column=0, padx=5, pady=5)
  field_frame.pack(padx=5, pady=5)

  window.mainloop()

if __name__ == '__main__': build_main()