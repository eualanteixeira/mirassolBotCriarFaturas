import time

import keyboard
from plyer import notification


class ControleExecucao:
    """Controle de pausar/continuar/parar de um processo em loop via hotkeys globais."""

    def __init__(self, subprocesso=None):
        self.pausado = False
        self.rodando = True
        self.subprocesso = subprocesso

    def alternar_pausa(self):
        self.pausado = not self.pausado

        if self.pausado:
            print("⏸ Automação pausada")
            self.notificar("Automação pausada")
        else:
            print("▶ Automação retomada")
            self.notificar("Automação retomada")

    def finalizar(self):
        print("⏹ Encerrando automação")
        self.rodando = False
        self.notificar("Automação encerrada")

        if self.subprocesso is not None:
            try:
                self.subprocesso.kill()
            except Exception as e:
                print(f"Erro ao encerrar subprocesso: {e}")

    def checkpoint(self):
        while self.pausado:
            time.sleep(0.2)

        if not self.rodando:
            raise SystemExit("Automação encerrada pelo usuário")

    def iniciar_hotkeys(self):
        keyboard.add_hotkey('ctrl+shift+space', self.alternar_pausa)
        keyboard.add_hotkey('ctrl+shift+q', self.finalizar)

    def notificar(self, mensagem):
        try:
            notification.notify(
                title="BotCriaFatura",
                app_name="BotCriaFatura",
                message=mensagem,
                timeout=3
            )
        except Exception as e:
            print(f"Erro ao exibir notificação: {e}")
