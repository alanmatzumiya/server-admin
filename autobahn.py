from __future__ import unicode_literals
import youtube_dl
import geckodriver_autoinstaller
from selenium.webdriver import Firefox, FirefoxOptions
import yaml
from time import sleep

geckodriver_autoinstaller.install()
options = FirefoxOptions()
options.headless = True


class BotDriver:


    @staticmethod
    def youtube_downloader(url):

        ydl_opts = {}
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except youtube_dl.utils.DownloadError or RecursionError:
            return None

    @staticmethod
    def youtube_search(name):

        driver = Firefox(options=options)
        driver.get('https://www.youtube.com/results?search_query=' + name)
        titles = driver.find_elements_by_id('video-title')
        song = {"name": titles[0].get_attribute("title"), "url": titles[0].get_attribute("href")}

        driver.close()
        return song

    def get_playlist(self, url_playlist, name, path):

        driver = Firefox(options=options)
        driver.get(url_playlist)
        sleep(1)
        playlist = {}
        titles = driver.find_elements_by_id('video-title')
        # for a in driver.find_elements_by_xpath('.//a'):
        for song in titles:
            name = song.get_attribute("title")
            url = song.get_attribute('href')
            playlist[name] = url
            self.youtube_downloader(url)
        driver.close()
        with open(path + name + ".yml", "w") as outfile:
            yaml.dump(playlist, outfile, default_flow_style=False)

