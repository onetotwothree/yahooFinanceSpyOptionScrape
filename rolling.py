import os
import yfinance as yf
import alpha_vantage as av
import pandas as pd
from datetime import datetime

class App:
    def __init__(self, enteredCmd):
        self.cmd = enteredCmd
        self.cmdList = ['shutdown', 'help', 'cnfgintg', 'collect', 'dailyfolderintg']
        self.dailyfldr = datetime.now().strftime('%Y-%m-%d')
        try:
            print('\nOpening files...')
            self.savefile = open('settings.txt', 'r')
            self.prevfile = open('previousresults.txt', 'w')
            print('\nSuccess')
        except IOError:
            print('\nOne or more file(s) is missing')
            print('\nAttempting to fix...')
            self.firstTimeLaunch()
        print('\nChecking for daily folder...')
        if os.path.isdir(datetime.now().strftime('%Y-%m-%d')):
            print('\nSuccess')
        else:
            print('\nDaily Folder doesn\'t exist')
            print('\nAttempting to fix...')
            self.dailyFolder()
        self.main()

    def yahooScrape():
        url = 'https://finance.yahoo.com/quote/SPY/options?p=SPY'
        html = requests.get(url).contentprint(html)

    def roundtofive(self, base=5):
        x = datetime.now().strftime('%H.%M')
        x = x.split('.')
        x[1] = int(x[1])
        x[1] = str(base * round(x[1]/base))
        return '.'.join(x)

    def nextPeriod(self):
        current_time = self.roundtofive()
        current_time = current_time.split('.')
        current_time[1] = int(current_time[1])
        current_time[1] += 5
        current_time[1] = str(current_time[1])
        return '.'.join(current_time)

    def dailyFolder(self):
        try:
            print('\nCreating daily folder...')
            os.mkdir(datetime.now().strftime('%Y-%m-%d'))
        except IOError:
            print('\nDaily folder exists or failed to create')

    def firstTimeLaunch(self):
        try:
            print('\nCreating settings.txt in', os.getcwd())
            self.savefile = open('settings.txt', 'x')
            self.savefile.close()
            self.savefile = open('settings.txt', 'r')
        except IOError:
            print('\nSettings file exists or couldn\'t be opened')
        try:
            print('\nCreating previousresults.txt in', os.getcwd())
            self.prevfile = open('previousresults.txt', 'x')
            self.prevfile.close()
            self.savefile = open('previousresults.txt', 'w')
        except IOError:
            print('\nPrevious results file exists or couldn\'t be opened')

    def shutdown(self):
        self.savefile.close()
        print("\nSettings file saved")
        self.prevfile.close()
        print("\nPrevious Results file saved")
        print("\nShutting down... ")

    def help(self):
        print('\nList of commands: \n')
        for i in self.cmdList:
            print(i + ' ', end='')
        print('')

    def strategyCollect(self):
        tckr = input("\nEnter Ticker: ")
        current_period = self.roundtofive()
        next_period = self.nextPeriod()
        while not current_period == next_period:
            if not os.path.isdir(self.dailyfldr + '\\' + str(current_period)):
                os.mkdir(self.dailyfldr + '\\' + str(current_period))
            else:
                print('\nCurrent period folder couldn\'t be created or exists')
            try:
                ticker = yf.Ticker(tckr)
                exp = ticker.options
                if not os.path.isdir(self.dailyfldr + '\\' + str(current_period) + '\\' + tckr):
                    os.mkdir(self.dailyfldr + '\\' + str(current_period) + '\\' + tckr)
                else:
                    print('\nCurrent Ticker folder couldn\'t be created or exists')
                for i in exp:
                    opt = ticker.option_chain(i)
                    opt.calls.to_csv(self.dailyfldr + '\\' + str(current_period) + '\\'+ tckr + '\\' + tckr + 'calls' + i + '.csv')
                    opt.puts.to_csv(self.dailyfldr + '\\' + str(current_period) + '\\' + tckr + '\\' + tckr + 'puts' + i + '.csv')
                    time.sleep(.300)
                current_period = next_period
            except:
                print('\nYahoo Finance may have failed...')
                break

    def main(self):
        while not self.cmd == 'shutdown':
            self.cmd = input("\nWhat is you next command: ")
            self.cmd = self.cmd.lower()
            if self.cmd in self.cmdList:
                if self.cmd == 'help':
                    self.help()
                if self.cmd == 'cnfgintg':
                    self.firstTimeLaunch()
                if self.cmd == 'collect':
                    try:
                        self.strategyCollect()
                    except ValueError:
                        print('Problem passing or splitting input')
                if self.cmd == 'dailyfolderintg':
                    self.dailyFolder()
            else:
                print('\nInvalid command entered')
        else:
            self.shutdown()

App('')
