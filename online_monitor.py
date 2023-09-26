#python3 -i online_monitor.py
import argparse
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os
import numpy as np 

import utilities.utilities as utils

options_parser = argparse.ArgumentParser(description = '')
options_parser.add_argument('-input_directory', '-d', default=None, type=str, help='input_directory')
options_parser.add_argument('-radius', '-r', default=None, type=int, help='ROI radius')


class EventHandler(FileSystemEventHandler):

    filesToProcess = []

    def on_modified(self, event):
        if (event.src_path).endswith('.txt') :

            for f in self.filesToProcess: 

                cmd = 'python3 process_image.py -f %s -p %s ' % (event.src_path, fiberPositionsFile)
                if roi_radius != None: 
                    cmd += ' -r %d' % roi_radius
                subprocess.run(cmd, shell = True)


                infoFile = utils.search_file_in_directory(directoryPath, '/info*.txt')
                info = utils.parse_config_file(infoFile, utils.DTYPE_DICT)
                #print('f: ', f, 'type f',)
                index = np.where(info['data_file']==os.path.basename(f))[0][0]
                #print('index: ', index)
                darkFile = directoryPath + info['dark_file'][index]
                #print('darkFile ', darkFile)
                dataFile = directoryPath + f
                #print('dataFile',dataFile)
                cmd = 'python3 process_image.py -f %s -d %s -p %s ' % (dataFile, darkFile, fiberPositionsFile)
                if roi_radius != None: 
                    cmd += ' -r %d' % roi_radius
                subprocess.run(cmd, shell = True)
                
        return 

    def on_created(self, event): 
        if (event.src_path).endswith('.TIF') :
            
            self.filesToProcess.append(os.path.basename(event.src_path))

            print('file saved. fileToProcessList:  ', self.filesToProcess)

            """
            cmd = 'python3 process_image.py -f %s -p %s ' % (event.src_path, fiberPositionsFile)
            if roi_radius != None: 
                cmd += ' -r %d' % roi_radius
            subprocess.run(cmd, shell = True)

            try:
                infoFile = utils.search_file_in_directory(directoryPath, '/info*.txt')
                info = utils.parse_config_file(infoFile, utils.DTYPE_DICT)

                index = np.where(info['data_file']==os.path.basename(event.src_path))[0]

                darkFile = directoryPath + info['dark_file'][index][0]
                cmd = 'python3 process_image.py -f %s -d %s -p %s ' % (event.src_path, darkFile, fiberPositionsFile)
                if roi_radius != None: 
                    cmd += ' -r %d' % roi_radius
                subprocess.run(cmd, shell = True)
            except:
                print('No analysis with dark subtraction performed\n')
                """
            return 
if __name__ == "__main__":
  
    options = vars(options_parser.parse_args())
    directoryPath = options['input_directory']
    roi_radius = options['radius']

    fiberPositionsFile = utils.search_file_in_directory(directoryPath, '/fiberPositions.txt')
    pos = utils.parse_config_file(fiberPositionsFile, utils.ROI_POS_DICT)

    infoFile = utils.search_file_in_directory(directoryPath, '/info*.txt')

    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, infoFile, recursive=False)
    observer.schedule(event_handler, directoryPath, recursive=False)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



 