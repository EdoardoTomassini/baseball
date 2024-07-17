import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceAnno = None
        self._choiceSquadra = None

    def handleCreaGrafo(self, e):
        anno = self._choiceAnno
        if anno is None:
            self._view._txt_result.controls.append(
                ft.Text("Selezionare un anno"))
            self._view.update_page()
            return
        self._model.buildGraph(anno)
        nN, nE = self._model.getGraphDetails()
        self._view._txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato"))
        self._view._txt_result.controls.append(
            ft.Text(f"Num nodi = {nN}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Num archi = {nE}"))

        self._view.update_page()

    def handleTeamsOfYear(self, e):
        self._view._txt_result.controls.clear()
        self._view._txtOutSquadre.controls.clear()
        anno = self._choiceAnno
        if anno is None:
            self._view._txt_result.controls.append(
                ft.Text("Selezionare un anno"))
            self._view.update_page()
            return
        teams = self._model.getAllTeamsOfYear(anno)
        self._model.getSalaryOfTeamPerYear(anno)
        numTeams = 0
        for t in teams:
            numTeams += 1
        self._view._txtOutSquadre.controls.append(
            ft.Text(f"Sono {numTeams} le squadre ad aver partecipato "
                    f"al campionato del {anno}"))
        for t in teams:
            #appendo il codice nella listview
            self._view._txtOutSquadre.controls.append(
                ft.Text(f"{t.teamCode}"))
            self._view._ddSquadra.options.append(
                ft.dropdown.Option(data=t,
                                   on_click=self.readDDSquadra,
                                   text=t.teamCode
                                   ))


        self._view.update_page()




    def handleDettagli(self, e):
        v0 = self._choiceSquadra
        vicini = self._model.getSortedNeighbours(v0)
        for v in vicini:
            self._view._txt_result.controls.append(
                ft.Text(f"{v[1]} - {v[0].name}"))

        self._view.update_page()

    def handlePercorso(self, e):
        pass

    def fillDDYear(self):
        years = self._model.getAllYears()
        for y in years:
            self._view._ddAnno.options.append(
                ft.dropdown.Option(data=y,
                                   on_click=self.readDDAnno,
                                   text=y
                                   ))

    def readDDAnno(self, e):
        self._view._ddSquadra.options.clear()
        anno = e.control.data
        if anno is None:
            self._view._txt_result.controls.append("Non è stato selezionato nessun anno")
            self._view.update_page()
        else:
          self._choiceAnno = anno


    def readDDSquadra(self, e):
        self._view._txt_result.controls.clear()
        team = e.control.data
        if team is None:
            self._view._txt_result.controls.append("Non è stato selezionato nessun anno")
            self._view.update_page()
        else:
          self._choiceSquadra = team

