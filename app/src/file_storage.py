import os
import json

class EventFileManager:
    FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'events.json')

    def read_events_from_file(self):
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, 'r') as file:
                events = json.load(file)
        else:
            events = []
        
        return events
    
    def write_events_to_file(self, events):
        with open(self.FILE_PATH, 'w') as file:
            json.dump(events, file)


        
    