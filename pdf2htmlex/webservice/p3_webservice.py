from tornado import web, ioloop
import json
import sys
import subprocess



def run_waiting_command(self,commando, f):
    try:
        retcode = subprocess.call(commando, shell=True)
        f.write("Corriendo programa...\n")
        if retcode < 0:
            print("Child was terminated by signal", -retcode, file=sys.stderr)
        else:
            f.write("Corriendo exitosa...\n")
            self.write("Programa en proceso")
            print("Piv corrido exitosamente. Exit Code: ", retcode, file=sys.stderr)
    except OSError as e:
        f.write("Excepcion...\n")
        self.write("Excepcion")
        print("Execution failed:", e, file = sys.stderr)

class PdfToHtmlEx(web.RequestHandler):

    def set_default_headers(self):
        print ("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        # self.set_header('Access-Control-Allow-Headers', 'X-CSRF-Token')

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
        except:
            response = {
                'success': 'false',
                'error': 'Ups, hubo un error'
            }

            response = json.dumps(response)
            self.write(response)

            #if hasattr(e, 'message'):
            #    response["message"] = e.message
            #else:

            #    print(e)




def execute_pdf_to_html_conversion ( command ):

    try:
        print("*************")
        print(command)
        MyOut = subprocess.Popen(command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)
        stdout,stderr = MyOut.communicate()
        print(stdout)
        print(stderr)



    except OSError as e:
        print(e)
        raise Exception(e)


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
        output_filename_command += options["output_name"] + ".html"

    command = initial_command + " /pdf/" + filename + output_filename_command;

    return command;
app = web.Application([
    (r"/pdf-to-html-conversion", PdfToHtmlEx),
])


if __name__ == '__main__':
    app.listen(8086)
    ioloop.IOLoop.instance().start()
