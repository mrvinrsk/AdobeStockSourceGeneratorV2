import datetime
import sys

from scrape_link import adobestock, flaticon, fallback

if __name__ == '__main__':
    # if file path is given as cli argument, use it for reading, otherwise use "sources.txt" in current directory
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "sources.txt"

    now = datetime.datetime.now()

    # format the date and time as a string
    date_string = now.strftime("%d.%m.%Y %H:%M")

    with open(file_path[:file_path.rfind(".")] + ".html", "a") as output:
        output.write("<div class='sources' data-last-updated='" + str(date_string) + '\'>\n')
        output.write("\t<!-- StockSourceGenerator by Marvin Roßkothen -->\n")

    # read each line as a source url
    with open(file_path, "r") as f:
        for line in f:
            url = line.strip().split("?")[0]  # URL without parameters

            if "stock.adobe.com" in url:
                link = adobestock(url)
            elif "flaticon.com" in url:
                link = flaticon(url)
            else:
                link = fallback(url)

            # write the link to a file in the same directory as the file being parsed (use absolute path). The
            # created file should be the same name as the file being parsed, but with ".html" as extension
            with open(file_path[:file_path.rfind(".")] + ".html", "a") as output:
                output.write("\t" + link)
                output.write("\n")

            print("Finished parsing & saved href for: " + url)

    with open(file_path[:file_path.rfind(".")] + ".html", "a") as output:
        output.write("</div>")
