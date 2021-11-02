from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from time import sleep
import re
import os.path

class ScrapLyrics:
	def __init__(self, artist: str):
		self.artist = artist
		self.base_song_names_url = 'http://www.song-list.net/%s/songs' %(artist)
		self.base_song_lyrics_url = 'https://www.azlyrics.com/lyrics/%s/{}.html' %(artist)

	def get_names(self):
		print('Getting song names...')
		song_names = []
		try:
			req = Request(self.base_song_names_url, headers={'User-Agent': 'Mozilla/5.0'})
			html_page = urlopen(req).read()
			soup = BeautifulSoup(html_page, 'html.parser')
			names = soup.find_all("div", {"class": "songname"})
			for name in names:
				try:
					extracted_name = name.find('a').contents[0]
					numbers_in_brackets_removed = re.sub(r'\(.*\)','', extracted_name)
					processed_song = re.sub(r'\W+', '', numbers_in_brackets_removed).lower()
					song_names.append(processed_song)
				except:
					pass
			print('Total song names found: ', len(song_names))
			return list(set(song_names))
		except:
			print('Error getting song names')
			return []
	
	def get_lyrics(self):
		print('Getting lyrics...')
		song_names = self.get_names()
		lyrics = ''
		success_count = 0
		for song in song_names:
			try:
				song_lyrics_url = self.base_song_lyrics_url.format(song)
				html_page = urlopen(song_lyrics_url)
				soup = BeautifulSoup(html_page, 'html.parser')

				html_pointer = soup.find('div', attrs={'class':'ringtone'})
				lyrics = lyrics + html_pointer.find_next('div').text.strip()
				success_count = success_count + 1
				print('%s passed' %(song))
			except:
				print('%s failed' %(song_lyrics_url))
			sleep(5)
		print('Success count for downloading lyrics: ', success_count, '/', len(song_names))
		return lyrics

	def create_lyrics_file(self):
		if os.path.isfile('%s.txt' %(self.artist)):
			print('File already present. Reusing it.')
			f = open("%s.txt" %(self.artist), "r")
			lyrics = f.read()
		else:
			lyrics = self.get_lyrics()
			with open("%s.txt" %(self.artist), "w") as text_file:
				text_file.write(lyrics)
		return lyrics