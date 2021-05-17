# Reddit Comic Downloader #

It's a utility that I did to download a comic from a specific subredit. Not very usefull but anyway sharing is caring.
Sorry but the code is in spanglish.

# Basic Usage #

To use it you have to copy **redditdownloader.config.example** to **redditdownloader.config**, and fill the parameters, you need a reddit account, and imgur account.

Also you will have to pip install -r requeriments.txt

And if you configured everything right just by executing 
```
./downloader.py
```

Optionally you can also specify configuration values as arguments if you don't want to do some of the confiugration.

```
usage: downloader.py [-h] [-s S] [-c C] [-o O] [-l L] [-g G]

optional arguments:
  -h, --help  show this help message and exit
  -s S        Indicar a continuacion el subreddit de donde quieres bajar las imagenes
  -c C        indicar un fichero de configuracion alternativo para la api de reddit, por defecto es redditdownloader.config
  -o O        indicar la carpeta donde se almacenara la descarga, por defecto sera la carpeta activa
  -l L        Para indicar el limite de posts de reddit que se miraran[int]
  -g G        Para indicar el limite de fotografias que van a sueltos[int]
```