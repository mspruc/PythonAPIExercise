import json
import npyscreen
import _curses
import requests
import time

url = "https://jobs.github.com/positions.json?"

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        #add forms to the application
        self.addForm('MAIN', FirstForm, name="Job_Box")
        print("app started")
        
class FirstForm(npyscreen.ActionFormMinimal):

    def printJobs(self, list):
        jobNames = []
        for i in range(len(list)):
            jobNames.append("[" + list[i]['company'] + " " +list[i]['title'] + "]")
        return jobNames

    def fetchBy(self, widget, list, type, typeName):
        sortedJobs = []

        if self.get_widget(widget).value:
            for i in range(len(list)):
                if list[i][type] == typeName:
                    sortedJobs.append(list[i])
        return sortedJobs

    def create(self):
        self.add(npyscreen.Checkbox, w_id="fullTime", name = "Check box if you are searching for full time jobs")
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

        #Sort fulltime or not
        resp1 = self.fetchBy("fullTime", resp, 'type', "Full Time")

        #Sort by language
        #resp2 = self.fetchBy("pgr", resp1, '')

        #Sort by location
        resp1 = self.fetchBy("loc", resp1, 'location', self.get_widget("loc").value)
        resp1 = self.printJobs(resp1)
        npyscreen.notify_confirm(str(resp1), title="List of Companies you can apply jobs at", wrap=True, wide=True, editw=1)



app = App()
app.run()