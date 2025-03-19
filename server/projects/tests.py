from django.test import TestCase
import requests, json


url = "http://127.0.0.1:8000/api/projects/ideas/create/"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyMzgyNDQzLCJpYXQiOjE3NDIzODE4NDMsImp0aSI6ImNmM2UyMjUxMzc1OTQyZDVhZDkwZGNhMzI2OTBjNmM3IiwidXNlcl9pZCI6NH0.a426ZACLng-Cogp90jwPvYVOIDILTSVhtObGXQu4azQ"

data = {
"headers": {
		"Authorization": f"Bearer ${token}",
		"Content-Type": "application/json"
		},

    "name": "Мой крутой стартап",
    "description": "Идея, которая изменит мир"

}

