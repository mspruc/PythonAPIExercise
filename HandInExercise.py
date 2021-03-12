import json
import npyscreen
import _curses
import requests
import time
from npyscreen import FixedText
from npyscreen.wgNMenuDisplay import HasMenus

url = "https://jobs.github.com/positions.json?"

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        #add forms to the application
        self.addForm('MAIN', FirstForm, name="main")
        print("app started")
 
class FirstForm(npyscreen.ActionFormMinimal, npyscreen.FormWithMenus):

    def drawLine(self,text,relx,rely):
        self.add(npyscreen.TitleText, w_id="sun", name=text,editable = False, relx = relx,rely = rely)

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
        #self.add(npyscreen.Checkbox, w_id="fullTime", name = "full time?")
        self.add(npyscreen.TitleText, w_id="pgr", name= "Enter your preferred programming language: " )
        self.add(npyscreen.TitleText, w_id="loc", name= "Enter your preferred location: " )
        self.add(npyscreen.FixedText, w_id="asdawdd",  value = "Hey " )
        test = self.add(npyscreen.ComboBox, w_id="sss", name= "test box")


        ascii =    ("--------------------------------------------------------- -",
                    "|                   .mmMMMMMMMMMMMMMmm.                   |",
                    "|               .mMMMMMMMMMMMMMMMMMMMMMMMm.               |",
                    "|            .mMMMMMMMMMMMMMMMMMMMMMMMMMMMMMm.            |",
                    "|          .MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM.          |",
                    "|        .MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM.        |",
                    "|       MMMMMMMM^      MMMM^^^^^^MMMM     ^MMMMMMMM       |",
                    "|      MMMMMMMMM                           MMMMMMMMM      |",
                    "|     MMMMMMMMMM:                         :MMMMMMMMMM     |",
                    "|    .MMMMMMMMMM                           MMMMMMMMMM.    |",
                    "|    MMMMMMMMM^                             ^MMMMMMMMM    |",
                    "|    MMMMMMMMM                               MMMMMMMMM    |",
                    "|    MMMMMMMMM                               MMMMMMMMM    |",
                    "|    MMMMMMMMMM                             MMMMMMMMMM    |",
                    "|    `MMMMMMMMMM                           MMMMMMMMMM`    |",
                    "|     MMMMMMMMMMMM.                     .MMMMMMMMMMMM     |",
                    "|      MMMMMM  MMMMMMMMMM         MMMMMMMMMMMMMMMMMM      |",
                    "|       MMMMMM  ^MMMMMMM           MMMMMMMMMMMMMMMM       |",
                    "|        `MMMMMM  ^MMMMM           MMMMMMMMMMMMMM`        |",
                    "|          `MMMMMm                 MMMMMMMMMMMM`          |",
                    "|            `^MMMMMMMMM           MMMMMMMMM^`            |",
                    "|               `^MMMMMM           MMMMMM^`               |",
                    "|                   `^^M           M^^`                   |",
                    "'---------------------------------------------------------'"
                   )

        for i in range(len(ascii)):
            self.drawLine(ascii[i],60,i)

        test.values = [i,len(ascii)]


        details = {
                'pgr' : self.get_widget("pgr").value,
                'loc' : self.get_widget("loc").value,
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