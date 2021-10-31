
import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]


class googleConnect:
    def __init__(self, sheetID, sheetTarget, jsonFile='gcgclassement_creds.json'):
       self.sheetID = sheetID
       self.sheetTarget = sheetTarget
       self.jsonFile = jsonFile
       self.worksheet=None   


    def googleLogin(self):
        print(f'Loading jsonFile')
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.jsonFile, scope)

        print(f'Authorizing connection')
        c_user = gspread.authorize(creds)
        
        print(f'Collecting sheetID')
        sh = c_user.open_by_key(self.sheetID)

        print(f'Selecting valid Sheet')
        self.worksheet = sh.worksheet(self.sheetTarget)
        print(f'fin slected sheet')
        
