import bisect
import event as ev
import random
##

class SimulationTime():
	def __init__(self):
		'''Used to keep track of the current simulation	time.
		'''
		self.time= 0.0
		
	def __str__(self):
		return '%8.4f' % (self.time)

		
class SimulationCalendar():
	def __init__(self):
		'''Simulation calendar that gets populated with events.
		'''
		self.calendar= []
		
	def __str__(self):
		cal= ''
		for evnt in self.calendar:
			cal += evnt.__str__()
			
		return cal
	
	def add_event(self, evnt):
		'''Insert the event into the (already sorted) simulation 
		calendar.  The custom sort defined in the Event class is
		used.
		'''
		bisect.insort(self.calendar, evnt)

	def handle_event(self, sim_time):
		'''To handle an event:
		1. update sim_time.time to reflect the current simulation 
			time (at which the event occurs), and
		2. remove the event from the simulation calendar.
		'''
		sim_time.time= self.calendar[0].occurrence_time
		
		next_event= self.calendar.pop(0)
		next_event.handle_event()	
