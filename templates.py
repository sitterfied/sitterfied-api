import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

modules = ['sitterfied']

thisdir = os.path.dirname(os.path.realpath(__file__))
module_dirs =  [os.path.join(thisdir, mod, "static_source", "js", "templates") for mod in modules]

def compile_templates():
    print "compiling templates..."
    for template_dir in module_dirs:
        #html_files = os.path.join(template_dir "*.html")
        all_files = os.path.join(template_dir, "*")

        dest_path = os.path.join(template_dir,  "..", "templates.js")

        print "compiling ", template_dir
        os.system("ember-precompile %s -f %s" % (all_files, dest_path))
        print "compiled ", template_dir
        with open(dest_path, 'r+') as fsock:
            content = fsock.read()
            fsock.seek(0)
            fsock.write("define(['ember'], function(Ember){")
            fsock.write(content)
            fsock.write('})')

        #os.system("rm %s" % (html_dir))


class Compiler(FileSystemEventHandler):
    def on_any_event(self, event):
        compile_templates()


if __name__ == "__main__":
    compile_templates()
    observer = Observer()
    compiler = Compiler()
    for module_dir in module_dirs:
         observer.schedule(compiler, module_dir)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
