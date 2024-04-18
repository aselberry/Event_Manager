from fastapi import APIRouter, HTTPException
from typing import List
from .models import Event
from .file_storage import EventFileManager 
from .event_analyzer import EventAnalyzer
import json

router = APIRouter()
event_manager = EventFileManager()
event_analyzer = EventAnalyzer()  

@router.get("/events", response_model=List[Event])
async def get_all_events():
    try:
        events = event_manager.read_events_from_file()
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(date: str = None, organizer: str = None, status: str = None, event_type: str = None):
    try:
        events = event_manager.read_events_from_file()
        filtered_events = events
        if date:
            filtered_events = [event for event in filtered_events if event.date == date]
        if organizer:
            filtered_events = [event for event in filtered_events if event.organizer.name == organizer]
        if event_type:
            filtered_events = [event for event in filtered_events if event.type == event_type]
        if status:
            filtered_events = [event for event in filtered_events if event.status == status]
        
        return filtered_events

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    event_manager = EventFileManager()
    events = event_manager.read_events_from_file()
    for event in events:
        if event.id == event_id:
            return event  
    
    raise HTTPException(status_code=404, detail="Event not found")
      

@router.post("/events", response_model=Event)
async def create_event(event: Event):
    events = event_manager.read_events_from_file()
    doesExist = False
    for eventToSearch in events:
        if eventToSearch.id == event.id:
            doesExist = True
            
    if(not doesExist):
        events.append(event)
        event_manager.write_events_to_file(events)
        print("New event has been created and inserted into the file")
    else:
        print("Event ID already exists")
            


@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    events = event_manager.read_events_from_file()
    doesExist = False
    for eventToSearch in events:
        if(eventToSearch.id == event_id):
            doesExist = True
            eventToSearch = event
       
    event_manager.write_events_to_file(events)
    if(doesExist):
        print("The event has been successfully updated!")
    else:
        print("The event does not exist!")
            
               
@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    events = event_manager.read_events_from_file()
    doesExist = False
    for event in events:
        if event.id == event_id:
            doesExist = True
            events.remove(event)
            break  

    event_manager.write_events_to_file(events)
    if (doesExist):
        return {"message": f"Event with ID {event_id} has been successfully deleted"}
    else:
        return {"message": f"Event with ID {event_id} does not exist"}


@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    events = event_manager.read_events_from_file()
    event_analyzer.get_joiners_multiple_meetings_method(events)
