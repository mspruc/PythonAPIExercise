import json
import npyscreen
import _curses
import requests
import time

url = "https://jobs.github.com/positions.json?"

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        #add forms to the application
        self.addForm('MAIN', FirstForm, name="main")
        print("app started")
        
class FirstForm(npyscreen.ActionFormMinimal):

    def fetchBy(self, widget, list, type, typeName):
        sortedJobs = []

        if self.get_widget(widget).value:
            for i in range(len(list)):
                if list[i][type] == typeName:
                    sortedJobs.append("[" + list[i]['company'] + " " +list[i]['title'] + "]")
        return sortedJobs

    def create(self):
        self.add(npyscreen.Checkbox, w_id="fullTime", name = "full time?")
        self.add(npyscreen.TitleText, w_id="pgr", name= "Enter your preferred programming language: " )
        self.add(npyscreen.TitleText, w_id="loc", name= "Enter your preferred location: " )

        details = {
                'pgr' : self.get_widget("pgr").value,
                'loc' : self.get_widget("loc").value
            }

        print("buttons created")


    def on_ok(self):
        print("user pressed ok button.")
        print(self.get_widget("fullTime").value)
        
        resp = requests.get(url=url)
        resp = resp.json()
        print(resp)

        #print(len(resp))
        #print(type(resp))
        #print(resp[0]['type'])

        resp1 = self.fetchBy("fullTime", resp, 'type', "Full Time")
        npyscreen.notify_confirm(str(resp1), title="List of Companies you can work at :)", wrap=True, wide=True, editw=1)



app = App()
app.run()