import json
import sys

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':

    # if file path is given as cli argument, use it for reading, otherwise use "sources.txt" in current directory
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "sources.txt"

    # read each line as a source url
    with open(file_path, "r") as f:
        for line in f:
            url = line.strip()
            # get the html content of the url
            html = requests.get(url).text
            # parse the html content
            soup = BeautifulSoup(html, "html.parser")

            # get script element with id "image-detail-json
            script = soup.find("script", {"id": "image-detail-json"})
            # get the content of the script element
            script_content = script.contents[0]

            # get image id from url (last part of url)
            image_id = url[url.rfind("/") + 1:]

            # parse the content as json
            _json = json.loads(script_content)

            title = _json[image_id]["title"]
            contributor = _json[image_id]["author"]

            # shorten the title to a max. of 50 characters, don't cut words
            title = title[:50]
            title = title[:title.rfind(" ")] + "..."

            print("Finished parsing: " + url)

            # create string with format: <a href="url" target="_blank">contributor - title</a>
            link = '<a href="' + url + '" target="_blank">' + contributor + " - " + title + "</a>"

            # write the link to a file in the same directory as the file being parsed (use absolute path). The created file should be the same name as the file being parsed, but with ".html" as extension
            with open(file_path[:file_path.rfind(".")] + ".html", "a") as output:
                output.write(link)
                output.write("\n")
