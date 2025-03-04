import csv
from icalendar import Calendar, Event,LocalTimezone
from datetime import datetime,timedelta
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, help='Укажите имя файл csv для конвертации в ics')
parser.add_argument('output', type=str, help='Укажите имя скорвертированного файла в формате ics')
args = parser.parse_args()

def csvToical(input_file, output_file):
    """Функциия конвертирует файл в формате csv в ics"""
    with open(input_file) as csv_file:
        reader = csv.reader(csv_file) 
        cal = Calendar()
        cal.add('prodid', '-//'+input_file+'//mxm.dk//')
        cal.add('version', '2.0')
        
        csv_data = []
        i = 0
        for row in reader:
            if i < 1:
                i += 1
                continue
            csv_data.append(row)
                
        for row in csv_data:
            event = Event()
            for index, items in enumerate(row):
                user = items.split(';')
                event.add('summary', str(user[6].strip()).encode('utf-8'))
                event.add('dtstart', datetime.strptime(user[1], '%d.%m.%Y'))
                event.add('dtend',   (datetime.strptime(user[3], '%d.%m.%Y')   + timedelta(days=1)).date())
                event.add('description', str(user[6].strip()).encode('utf-8'))
                event.add('location', 'Ukraine') 
                event.add('transp', 'TRANSPARENT')
                event.add('dtstamp', datetime.replace( datetime.now(), tzinfo=LocalTimezone() ))
            cal.add_component(event)
           
        with open(output_file, 'w') as out_f:
            out_f.write(cal.to_ical().decode('utf-8'))
            out_f.close()

def main(args):
  csvToical(args.input, args.output)
  
if __name__ == "__main__":
  main(parser.parse_args())

    
    
