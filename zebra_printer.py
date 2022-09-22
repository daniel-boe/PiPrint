from asyncio import subprocess
from logging import exception
import yaml
from subprocess import run
from pathlib import Path
from loguru import logger as log

class ZebraPrinter:

    def __init__(self) -> None:
        config = self.load_config()
        self.printer = config.get('targetPrinter')

    def load_config(self):
        try:
            config = yaml.safe_load(Path('printer-config.yaml').read_text())
        except FileNotFoundError:
            log.warning('No Printer Configuration file found')
            config = {}

        return config

    def print(self,zpl_file,n = 2):
        log.info(f'Printing {n} copies of {zpl_file} on {self.printer}')
        name  = Path(zpl_file).stem
        cmd  = ['lp','-d', self.printer,'-o', 'raw',zpl_file, '-n', str(n), '-t', f'"{name}"']
        try:
            process = run(cmd,timeout=5,check=True)
            status = process.returncode
        except subprocess.TimeoutExpired:
            log.error('Print job timed out')
            status = 1
        except subprocess.CalledProcessError:
            log.error('Print job was unsuccesful')        
            status = 1

        return not status

    def print_test_label(self):
        self.print('test-label.zpl')

if __name__ == '__main__':
    z = ZebraPrinter()
    z.print_test_label()