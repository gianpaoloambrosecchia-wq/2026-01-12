import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def riempiddAnno(self):
        anni = self._model.getAllYears()
        for a in anni:
            self._view._ddAnno1.options.append(
                ft.dropdown.Option(a)
            )
        for a in anni:
            self._view._ddAnno2.options.append(
                ft.dropdown.Option(a)
            )



    def handleCreaGrafo(self,e):
        anno1 = self._view._ddAnno1.value
        anno2 = self._view._ddAnno2.value

        if anno1 is None or anno2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione inserire il range di anni", color="red")
            )
            self._view.update_page()
            return

        self._model.buildGrafo(int(anno1),int(anno2))
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Grafo creato correttamente", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi")
        )
        self._view.update_page()

    def handleDettagli(self, e):
        primiTreArchi = self._model.getPrimiTreArchi()
        self._view.txt_result.controls.append(
            ft.Text("Archi di peso maggiore", color="red")
        )
        for e in primiTreArchi:
            self._view.txt_result.controls.append(
                ft.Text(f"{e[0]} --->{e[1]} ({e[2]["weight"]} piloti condivisi)")
            )


        lenC, componenteGrande, nodi_ordinati = self._model.infoConnessa()
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {lenC} componenti connesse", color="red")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Componente più grande ({len(componenteGrande)} nodi):")
        )
        for c in componenteGrande:
            self._view.txt_result.controls.append(
                ft.Text(c)
            )

        self._view.txt_result.controls.append(
            ft.Text("Componente connessa in ordine decrescente: ")
        )
        for n in nodi_ordinati:
            self._view.txt_result.controls.append(
                ft.Text(f"{n} (grado = {self._model._graph.degree(n)})")
            )
        self._view.update_page()


    def handleCerca(self, e):
        pass

