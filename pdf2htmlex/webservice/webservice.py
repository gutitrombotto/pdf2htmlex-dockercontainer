from tornado import web, ioloop
import json
import sys
import shlex, subprocess
import traceback
import logging
import os.path

class PdfToHtmlEx(web.RequestHandler):

    def post(self):

        post_body = json.loads(self.request.body.decode("utf-8"))
        #data = tornado.escape.json_decode(self.request.body)
        #print(post_body)

        filename = post_body["filename"]
        options = post_body["options"]
        command = generate_pdfToHtmlExCommand(filename, options)
        print(command)

        try:
            execute_pdf_to_html_conversion(command)
            response = {
                'success': 'true',
            }

            response = json.dumps(response)
            self.write(response)
        except Exception as e:
            logging.error(traceback.format_exc())
            error_message = traceback.format_exc()
            response = {
                'success': 'false',
                'error': error_message
            }

            response = json.dumps(response)
            self.write(response)


def execute_pdf_to_html_conversion ( command ):

    command = shlex.split(command)
    MyOut = subprocess.Popen(command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
    stdout,stderr = MyOut.communicate()


def generate_pdfToHtmlExCommand(filename, options):
    
    initial_command = 'pdf2htmlEX'
    
    initial_command += " --embed-font " + str(options["embed_font"])
    initial_command += " --embed-image " + str(options["embed_image"])
    initial_command += " --embed-javascript " + str(options["embed_javascript"])
    initial_command += " --embed-css " + str(options["embed_css"])
    initial_command += " --process-outline " + str(options["sidebar"])
    
    if options["embed_css"] == 0:
        style_output_filename = " --css-filename "
        
        if "output_name" in options:
            style_output_filename += options["output_name"] 
        else:
            style_output_filename += filename
            
        initial_command += style_output_filename + ".style.html"         

    if "width" in options:
        width_command = " --fit-width " + options["width"]
        initial_command += width_command
    
    output_filename_command = " "
    if "output_name" in options:
        output_filename_command += options["output_name"]
    else:
        filename_html_path  = os.path.splitext(filename)[0] + ".html"
        output_filename_command += filename_html_path

    command = initial_command + " /pdf/" + filename + output_filename_command;

    return command;
app = web.Application([
    (r"/pdf-to-html-conversion", PdfToHtmlEx),
])


if __name__ == '__main__':
    app.listen(8085)
    ioloop.IOLoop.instance().start()
