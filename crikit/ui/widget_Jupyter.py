"""
Created on Wed Mar  2 17:12:54 2016

@author: chc
"""

import os
os.environ['QT_API'] = 'pyqt5'

from PyQt5 import QtWidgets
from PyQt5 import QtGui
# ipython won't work if this is not correctly installed. And the error message will be misleading
from PyQt5 import QtSvg 

# Import the console machinery from ipython
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager
#from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
#from IPython.qt.inprocess import QtInProcessKernelManager


class QJupyterWidget(RichJupyterWidget):
    """ Convenience class for a live IPython console widget. We can replace the standard banner using the customBanner argument"""
    def __init__(self,customBanner=None,*args,**kwargs):
        super(QJupyterWidget, self).__init__(*args,**kwargs)
        if customBanner!=None: 
            self.banner=customBanner
        self.kernel_manager = kernel_manager = QtInProcessKernelManager()
        kernel_manager.start_kernel()
        def _abort_queues(kernel):
            # ! See IPython Issue: https://github.com/ipython/ipykernel/issues/370
            pass
        kernel_manager.kernel._abort_queues = _abort_queues
        kernel_manager.kernel.gui = 'qt'
        
        self.kernel_client = kernel_client = self._kernel_manager.client()
        kernel_client.start_channels()

        def stop():
            kernel_client.stop_channels()
            kernel_manager.shutdown_kernel()
            #get_app_qt5().exit()            
        self.exit_requested.connect(stop)

    def pushVariables(self,variableDict):
        """ Given a dictionary containing name / value pairs, push those variables to the IPython console widget """
        self.kernel_manager.kernel.shell.push(variableDict)
    def clearTerminal(self):
        """ Clears the terminal """
        self._control.clear()    
    def printText(self,text):
        """ Prints some plain text to the console """
        self._append_plain_text(text, False)
        
        
        
    def executeCommand(self,command):
        """ Execute a command in the frame of the console widget """
        self._execute(command,False)
        
if __name__ == '__main__':
    class ExampleWidget(QtWidgets.QMainWindow):
        """ Main GUI Window including a button and IPython Console widget inside vertical layout """
        def __init__(self, parent=None):
            super(ExampleWidget, self).__init__(parent)
            self.setWindowTitle('iPython in PyQt5 app example')
            self.mainWidget = QtWidgets.QWidget(self)
            self.setCentralWidget(self.mainWidget)
            layout = QtWidgets.QVBoxLayout(self.mainWidget)
            self.button = QtWidgets.QPushButton('Another widget')
            self.ipyConsole = QJupyterWidget(customBanner="Welcome to the embedded ipython console\n")
            layout.addWidget(self.button)
            layout.addWidget(self.ipyConsole)        
            # This allows the variable foo and method print_process_id to be accessed from the ipython console
            self.ipyConsole.pushVariables({"foo":43,"print_process_id":print_process_id})
            self.ipyConsole.printText("The variable 'foo' and the method 'print_process_id()' are available. Use the 'whos' command for information.\n\nTo push variables run this before starting the UI:\n ipyConsole.pushVariables({\"foo\":43,\"print_process_id\":print_process_id})")
            self.setGeometry(300, 300, 800, 600)

    def print_process_id():
        print('Process ID is:', os.getpid())
    
    def get_app_qt5(*args, **kwargs):
        """Create a new qt5 app or return an existing one."""
        app = QtWidgets.QApplication.instance()
        if app is None:
            if not args:
                args = ([''],)
            app = QtWidgets.QApplication(*args, **kwargs)
        return app
        

    app  = get_app_qt5()
    widget = ExampleWidget()
      
    widget.show()
    
   
    app.exec_()
    
    