# drawio_sync_img

Synchronizes the pages of a drawio document. 
The script saves each page in an image with the same page name.

## Setup 

- install drawio software (need drawio commands line) refer to: [https://github.com/jgraph/drawio-desktop/releases/](https://github.com/jgraph/drawio-desktop/releases/) 

- use the script such as a command line, inside your bashrc or zshrc insert the following line: 
```bash
export PATH=$PATH:/path/this/folder
```

## Use

Run the following command
```
$ drawio_sync_img -f path/to/drawio/file -o path/output/folder {-a} {-p x} {-t x}
# x = number
$ drawio_sync_img --help
usage: drawio_sync_img.py [-h] -f FILE [-o OUTPUT] [-a] [-p PAGE] [-t THREADS]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  drawio file to sync
  -o OUTPUT, --output OUTPUT
                        folder where image will be saved
  -a, --all-pages       sync all pages from the drawio file
  -p PAGE, --page PAGE  sync specific page number from the drawio file
  -t THREADS, --threads THREADS
                        threads number
```



