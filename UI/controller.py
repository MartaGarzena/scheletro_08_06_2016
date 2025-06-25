import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDYear(self):
        for a in self._model.getYears():
            self._view._ddAnno.options.append(ft.dropdown.Option(a))

    def handleSelezionaStagione(self, e):
        a = self._view._ddAnno.value
        if a is None:
            self._view.txt_result.controls.append(ft.Text("Inserire l'anno", color="red"))
            return

        self._model.buildGraph(int(a))
        vertici, archi = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(
            f"Numero di vertici: {vertici} Numero di archi: {archi}"))

        for a in self._model.getGare():
            self._view._ddGara.options.append(ft.dropdown.Option(a))

        arcoMax = self._model.getArcoMax()
        while len(arcoMax) > 0:
            self._view.txt_result.controls.append(ft.Text(
                f"arco massimo {arcoMax[0]}"))
            arcoMax.pop(0)

        self._view.update_page()

    def handleSimulaGara(self, e):
        print("controller, chiacchiato simula gara")

        pr = self._view._txtValoreP.value.strip()
        tm = self._view._txtValoreT.value.strip()

        if  tm.isdigit():  # Verifica che sia composto solo da cifre
            probabilita = float(pr)
            tempoProb = int(tm)
        else:
            self._view.txt_result.controls.append(ft.Text("Inserire un numero valido", color="red"))
            self._view.update_page()
            return

        a = self._view._ddGara.value
        if a is None:
            self._view.txt_result.controls.append(ft.Text("Inserire la gara", color="red"))
            self._view.update_page()
            return
        print("controlli passati")
        punti = self._model.simulazioneGara(int(a), probabilita, tempoProb)
        # --- Mostra classifica finale ---
        self._view.txt_result.controls.append(ft.Text("Classifica finale per punti (leader di giro):"))
        for driver, score in sorted(punti.items(), key=lambda x: x[1], reverse=True):
            self._view.txt_result.controls.append(ft.Text(f"Pilota {driver}: {score} punti"))

        self._view.update_page()
