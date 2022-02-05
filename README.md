# Github Sub Directory Downloader

Have you ever wanted to download just a sub directory from a GitHub repository? Sometimes it's necessary that we just grab a few files from a large project.

Unfortunately, GitHub doesn't support this out of the box, but you can easily done it with this simple tool.
  
# CLI-Tool


## Arguments

### positional arguments:

- **url**:  The url of the github repository

### optional arguments:

- **-h** or **--help**: show this help message and exit

- **-p** or **--path**: The path to download the files


## Using

```
python get_github_files.py {sub-dir-url} -p {download-path}
```

## Sample

```console 

foo@bar:~$ python get_github_files.py https://github.com/One-fifty-150/Github-Sub-Directory-Downloader/tree/main/sample_dir -p ~\downloads

>>> Total Size: 196.2KiB

>>> Downloaded ~\downloads\1.jpg
>>> Downloaded ~\downloads\2.jpg
>>> Downloaded ~\downloads\3.jpg
>>> Downloaded ~\downloads\4.jpg
>>> Downloaded ~\downloads\5.jpg

>>> ===Download Finished===

```

 ***Last Updated: 5 Feb, 2022***     