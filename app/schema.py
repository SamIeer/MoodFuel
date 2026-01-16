from pydantic import BaseModel
# Modle Schema
class MoodInput(BaseModel):
    sleep_hours: float
    stress_level: int
    time_of_day: int 
    workload_level: int

'''
This ensures clean, validated input data -- no missing or invalid fields when someone hits your API
'''