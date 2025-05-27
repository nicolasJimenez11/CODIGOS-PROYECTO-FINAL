class InterruptController:
    def __init__(self):
        self.pending = []
        self.handler_address = 0x80
        self.interrupt_enabled = True

    def raise_interrupt(self, code):
        if self.interrupt_enabled:
            self.pending.append(code)

    def check_and_handle(self, cpu):
        if self.pending:
            print("⚠️ Interrupción recibida. Código:", self.pending.pop(0))
            # Guarda PC actual
            cpu.registers["RA"] = cpu.PC
            cpu.PC = self.handler_address
            cpu.flush_pipeline()
