import yaml
import subprocess
from pathlib import Path
from loguru import logger as log
from shutil import copy2

PROGRAM_PATH = Path.home() / 'PiPrintData'
PROGRAM_PATH.mkdir(parents=True,exist_ok=True)
LABELS_PATH = PROGRAM_PATH / 'labels'
LABELS_PATH.mkdir(exist_ok=True)
CONFIG_PATH = PROGRAM_PATH / 'printer-config.yaml'

ROOT = Path(__file__).resolve().parent

log.add(PROGRAM_PATH / 'ZebraPrinter.log',backtrace=True, diagnose=True,level='INFO',retention='10 days',rotation = '1 day')

def initialize_label_folder():
    current_labels = [f.name for f in LABELS_PATH.iterdir() if f.is_file()]
    templates = [label for label in Path('label-templates').iterdir() if label.name not in current_labels] 
    for label in templates:
        contents = label.read_text()
        p =  LABELS_PATH / label.name
        p.write_text(contents)

class ZebraPrinter:

    def __init__(self) -> None:
        self.load_label_files()
        config = self.load_config()
        self.printer = config.get('targetPrinter')

    def load_config(self):
        try:
            config = yaml.safe_load(CONFIG_PATH.read_text())
        except FileNotFoundError:
            log.warning('No Printer Configuration file found')
            config = yaml.safe_load(Path('printer-config-sample.yaml').read_text())
        return config

    def _print(self,zpl_file,n = 1):
        log.info(f'Printing {n} copies of {zpl_file} on {self.printer}')
        name  = Path(zpl_file).stem
        cmd  = ['lp','-d', self.printer,'-o', 'raw',zpl_file, '-n', str(n), '-t', f'"{name}"']
        try:
            process = subprocess.run(cmd,timeout=5,check=True)
            status = process.returncode
        except subprocess.TimeoutExpired:
            log.error('Print job timed out')
            status = 1
        except subprocess.CalledProcessError:
            log.error('Print job was unsuccesful')        
            status = 1

        return not status

    def print_test_label(self):
        self._print(self.label_files.get('test-label'))
    
    def print_label(self,name,n = 2,**kwargs):
        if name not in self.label_files:
            log.warning(f'{name} is not available')
            raise FileNotFoundError(f'{name} not found')
        if kwargs:
            log.info('Args supplied, modifying label')
            zpl = self.label_files.get(name).read_text()
            with open(self.label_files.get('custom-label'),'w') as f:
                f.write(zpl.format(**kwargs))
            self._print(self.label_files.get('custom-label'),n=n)
        else:
            self._print(self.label_files.get(name),n=n)
            
    @classmethod
    def load_label_files(cls):
        cls.label_files = {f.stem:f for f in LABELS_PATH.iterdir() if f.suffix == '.zpl'}

    @classmethod
    def store_new_file(cls,filename,content):
        with open(LABELS_PATH / filename,'wb') as f:
            f.write(content)
        cls.load_label_files()        

if __name__ == '__main__':
    if not CONFIG_PATH.exists():
        copy2(ROOT / 'printer-config-sample.yaml',CONFIG_PATH)

    initialize_label_folder()
    z = ZebraPrinter()
    z.print_test_label()