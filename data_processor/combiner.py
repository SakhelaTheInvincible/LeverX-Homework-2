from typing import List, Dict, Any

class DataCombiner:
    def __init__(self, rooms: List[Dict[str, Any]], students: List[Dict[str, Any]]):
        self.rooms = rooms
        self.students = students

    def combine(self) -> List[Dict[str, Any]]:
        room_dict = {room['id']: {'id': room['id'], 'name': room['name'], 'students': []} 
                    for room in self.rooms}
        
        for student in self.students:
            room_id = student['room']
            if room_id in room_dict:
                room_dict[room_id]['students'].append({
                    'id': student['id'],
                    'name': student['name']
                })
        
        return list(room_dict.values())