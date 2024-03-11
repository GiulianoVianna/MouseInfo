import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import pyqtSignal
from pynput import mouse
from PIL import ImageGrab

class AplicacaoMouseInfo(QtWidgets.QMainWindow):
    # Sinal personalizado para comunicação entre eventos do mouse e a interface.
    sinal_mouse = pyqtSignal(str)

    def __init__(self):
        """Inicializa a aplicação e configura a interface gráfica."""
        super().__init__()
        self.janela = uic.loadUi("mouseinfo.ui")
        self.janela.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.rastreamento_ativo = False
        self.janela.bt_iniciar.clicked.connect(self.toggle_rastreamento)
        self.sinal_mouse.connect(self.atualizar_texto)

    def atualizar_texto(self, texto):
        """Atualiza o campo de texto na interface com informações sobre eventos do mouse."""
        self.janela.txt_local_mouse.setText(texto)

    def capturar_cor(self, x, y):
        """Captura a cor do pixel na posição especificada do cursor."""
        tela = ImageGrab.grab(bbox=(x, y, x+1, y+1))
        cor = tela.getpixel((0, 0))
        return cor

    def ao_mover(self, x, y):
        """Callback para eventos de movimento do mouse, atualiza informações na interface."""
        if not self.rastreamento_ativo:
            return
        cor = self.capturar_cor(x, y)
        info_texto = f'  Posição: ({x}, {y}) | Cor RGB : {cor}'
        self.janela.lb_mov_mouse.setText(info_texto)

    def ao_clicar(self, x, y, button, pressed):
        """Callback para eventos de clique do mouse, captura a cor no local do clique e emite um sinal com as informações."""
        if not self.rastreamento_ativo or not pressed:
            return
        cor = self.capturar_cor(x, y)  
        texto = f'Posição: ({x}, {y}) - Cor RGB: {cor}'  
        self.sinal_mouse.emit(texto)  


    def toggle_rastreamento(self):
        """Altera o estado de rastreamento do mouse, ativando ou desativando-o."""
        self.rastreamento_ativo = not self.rastreamento_ativo
        bt_iniciar = self.janela.bt_iniciar
        if self.rastreamento_ativo:
            bt_iniciar.setStyleSheet("background-color: red")
            bt_iniciar.setText("Parar")
        else:
            bt_iniciar.setStyleSheet("background-color: none")
            bt_iniciar.setText("Iniciar")

    def iniciar_monitoramento_mouse(self):
        """Inicia o monitoramento de eventos do mouse em uma thread separada."""
        listener = mouse.Listener(on_move=self.ao_mover, on_click=self.ao_clicar)
        listener.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    aplicacao = AplicacaoMouseInfo()
    aplicacao.janela.show()
    aplicacao.iniciar_monitoramento_mouse()
    sys.exit(app.exec_())
