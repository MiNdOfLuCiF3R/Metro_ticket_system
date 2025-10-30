
import pandas as pd
from uuid import uuid4
STATIONS_FILE = 'data/stations.csv'
LINES_FILE = 'data/lines.csv'
TICKETS_FILE = 'data/tickets.csv'
BASE_FARE = 10
class Station:
    
    def __init__(self, id, name, lines_str):
        self.id = id
        self.name = name
        self.lines = [line.strip() for line in str(lines_str).split(';') if line.strip()]

    def __repr__(self):
        return self.name

class MetroLine:
  
    def __init__(self, id, name, stations_str):
        self.id = id
        self.name = name
        self.stations = [station.strip() for station in str(stations_str).split(';') if station.strip()]

class Ticket:
    
    def __init__(self, start_station, end_station, price, path, instructions):
        self.ticket_id = str(uuid4())
        self.start_station = start_station
        self.end_station = end_station
        self.price = price
        self.path = path
        self.instructions = instructions

    def to_dict(self):
       
        return {
            'ticket_id': self.ticket_id,
            'start_station': self.start_station,
            'end_station': self.end_station,
            'price': self.price,
            
            'path': str(self.path), 
            'instructions': str(self.instructions) 
        }

def load_data():
    
    try:
      
        stations_df = pd.read_csv(STATIONS_FILE)
        stations = {
            row['name']: Station(row['id'], row['name'], row['lines'])
            for _, row in stations_df.iterrows()
        }

        lines_df = pd.read_csv(LINES_FILE)
        lines = {
            row['name']: MetroLine(row['id'], row['name'], row['stations'])
            for _, row in lines_df.iterrows()
        }
        
        try:
            tickets_df = pd.read_csv(TICKETS_FILE)
        except pd.errors.EmptyDataError:
            tickets_df = pd.DataFrame()

    except FileNotFoundError as e:
        print(f"Error: data file not found{e}")
        return None, None, None
    except Exception as e:
        
        print(f"An error occurred loading data: {e}")
        return None, None, None
        
    return stations, lines, tickets_df

def save_ticket(ticket: Ticket):
    
    try:
        new_ticket_df = pd.DataFrame([ticket.to_dict()])
        
       
        try:
            pd.read_csv(TICKETS_FILE)
            write_header = False
        except (pd.errors.EmptyDataError, FileNotFoundError):
            write_header = True 

        new_ticket_df.to_csv(TICKETS_FILE, mode='a', header=write_header, index=False)
    except Exception as e:
        print(f"Error saving ticket: {e}")