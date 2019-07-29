
# Pdf2HtmlEx - Dockerized
This is a dockerized solution for converting Pdf to Html Files. This software uses alpine container from the [Coolwalnglu repository Pdf2HtmlEX](https://github.com/coolwanglu/pdf2htmlEX).


## Installation

In order to get this container running, you should install [Docker]([https://docs.docker.com/install/](https://docs.docker.com/install/))  and [docker-compose]([https://docs.docker.com/v17.09/compose/install/](https://docs.docker.com/v17.09/compose/install/)/).

After that you should:
```bash
cd projectDirectory
docker-compose up -d
```

You will have the pdf2HtmlEx container running.

## Usage

Pdf2HtmlEx cointainer, will run a light webserver with [Tornado](https://www.tornadoweb.org/en/stable/).
So you should make a POST Http request with the filename and the parameters for the conversion as follows:

 - Make a Post request to http://localhost:8085/pdf-to-html-conversion
 - Set Header 
```json
{
	"Content-type": "application/json"
}
```
 - On the Request body, you can set the following options: 
```json
{
	"options": {
		"embed_font": 1,
		"embed_image": 1,
		"embed_css": 1,
		"embed_javascript": 1,
		"sidebar": 1
	},
	 "filename":"filename.pdf"
 }

```
 - After a success conversion, the converted file will be stored in the shared folder 


### Things to keep in mind

 1. The file to convert should be placed on the shared folder of this project directory. The filename in the Json Post must be set with the .pdf extension.
 2. There some other conversion options but currently are not allowed. You can see all of them in [Pdf2HtmlEx Wiki](https://github.com/coolwanglu/pdf2htmlEX/wiki/Command-Line-Options)

 
## Contributing
There are lots of things to improve. Pull requests are welcome. 
Some features to add are:

 - More Conversion options on the Post request. You be changed on webservice.py file.
 - Exceptions catching. Error responses.
 - Make the container initialization more parameterizable.



## License
[MIT](https://choosealicense.com/licenses/mit/)
