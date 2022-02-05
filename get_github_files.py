"""
Get GitHub Sub Directory
~~~~~~~~~~~~~~~~~~~~~

Have you ever wanted to download just a sub directory from a GitHub repository? Sometimes it's necessary that we just grab a few files from a large project.

Unfortunately, GitHub doesn't support this out of the box, but you can easily done it with this simple tool.

"""

from re import search
from requests import get
from pathlib import Path
from argparse import ArgumentParser


class NotValidGithubUrl(Exception):

    pass
    
class NotGithubSubDirUrl(Exception):

    pass

class GetGithubFiles:

    def __init__(self, url,cli=False):

        
        self.ls_download_url =  [] # raw content url
        self.ls_name = [] # file name
        self.ls_fronend_url = [] # Github frontend url
        self.total_size = 0  # total size of the files

        self._main(url)


    def _file_tree_url(self, url)->str:


        try:
            user, repository, ref, directory = search(r"[/]([^/]+)[/]([^/]+)[/]tree[/]([^/]+)[/](.*)",url ).groups()

            url = f"https://api.github.com/repos/{user}/{repository}/contents/{directory}?ref={ref}"

            return url

        except AttributeError:
            raise NotGithubSubDirUrl("The url is not a valid github sub dir!!!")

        

    def _fetch(self,url)->dict:
        
        response = get(url)

        if not response.ok :
            raise NotValidGithubUrl("Not a valid github repo url!!!")
        
        return response.json()


    def _parse_tree(self,tree):

        ls_size= []

        for i in tree:
            dowload_url = i.get("download_url")

            if dowload_url:
                self.ls_download_url.append(dowload_url)
                self.ls_name.append(i.get("name"))
                self.ls_fronend_url.append(i.get("html_url"))
                ls_size.append(i.get("size"))

        self.total_size =  sum(ls_size)



    def _main(self,url):

        self._file_tree_url = self._file_tree_url(url)
        self.files = self._fetch(self._file_tree_url)
        self._parse_tree(self.files)

    def _sizeof_fmt(self,num, suffix="B"):

        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024.0

        return f"{num:.1f}Yi{suffix}"

    def download_all(self,path="."):

        p = Path(path)
        p.exists() or p.mkdir(parents=True)

        print(f"Total Size: {self._sizeof_fmt(self.total_size)}",end="\n\n")

        for i in range(len(self.ls_download_url)):
            print(f"Downloading {self.ls_name[i]}", end="\r")
            dest = p / self.ls_name[i]

            with open(dest, 'wb') as file:
                file.write(get(self.ls_download_url[i]).content)
                print(f"Downloaded {dest}")

        print("\n===Download Finished===")


def main():


    parser = ArgumentParser(description="Download files from a github repository")
    parser.add_argument("url", help="The url of the github repository", type=str)
    parser.add_argument("-p","--path", help="The path to download the files", type=str, default=".\\",required=False)
    args = parser.parse_args()

    git = GetGithubFiles(args.url)

        
    git.download_all(args.path)



    
    

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print("\n===Download Interrupted===")
        exit()

    except NotValidGithubUrl:
        print("\n===Download Failed===")
        print("\nCan not get this repo, make sure you've provide a Github repo url, or check internet access.")
        exit()
    except NotGithubSubDirUrl:
        print("\n===Download Failed===")
        print("\nIt seems that you've provided a url that is not a valid github sub dir url.")
        exit()
        
    except Exception as e:
        print(e)
        exit()

 