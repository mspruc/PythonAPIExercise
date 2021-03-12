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
 
class FirstForm(npyscreen.ActionFormMinimal, npyscreen.FormWithMenus):

    test = None

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
        return list


    

    def create(self):
        self.add(npyscreen.FixedText, w_id="welcometxt",  value = "This is a jobsorter. Please insert your prefered jobvalues below. Good luck." )
        self.add(npyscreen.Checkbox, w_id="fullTime", name = "full time?")
        self.add(npyscreen.TitleText, w_id="loc", name= "Enter your preferred location: " )
        self.add(npyscreen.FixedText, w_id="pgrtext",  value = "Choose your preferred langauge below:" )
        self.test = self.add(npyscreen.ComboBox, w_id="pgr", name= "Enter your preferred programming language: ")


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

        for i in range(3,len(ascii)):
            self.drawLine(ascii[i],60,i)

        self.test.values = ["java", "c++", "python"]

        details = { #Check if we use
                'pgr' : self.get_widget("pgr").value,
                'loc' : self.get_widget("loc").value,
           }




    def on_ok(self):

        #Get API json file
        resp = requests.get(url=url)
        resp = resp.json()

        #Sort fulltime or not
        resp1 = self.fetchBy("fullTime", resp, 'type', "Full Time")

        #Sort by language
        if(self.get_widget("pgr").value):
            sortedJobs = []
            for i in range(len(resp1)):
                if self.test.values[self.get_widget("pgr").value] in resp1[i]['description']:
                    sortedJobs.append(resp1[i])
            resp1 = sortedJobs

        #Sort by location
        resp1 = self.fetchBy("loc", resp1, 'location', self.get_widget("loc").value)


        #Make it easier to read when printed, only gets company name
        resp1 = self.printJobs(resp1)

        #Prints the jobs on screen
        npyscreen.notify_confirm(str(resp1), title="List of Companies you can apply jobs at", wrap=True, wide=True, editw=1)



app = App()
app.run()