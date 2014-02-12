##

class Event():
	EVENT_METHODS= {'go_to_hole': 1,
					'play_hole': 2,
					'finish_hole': 3}
					
	def __init__(self, object, method, args, occurrence_time):
		'''An event is defined by:
		object: the object that has an event occur
		method: the method of the object
		args: a list of arguments to the method
		occurrence_time: the occurrence time of the event
		'''
		self.object= object
		self.method= method
		self.args= args
		self.occurrence_time= occurrence_time
		
	def __str__(self):
		return '%8.3f: %s - %s\n' \
				% \
				(self.occurrence_time, self.object.log_label,
				self.method)

	def __cmp__(self, other):
		'''Custom comparison used to order events in the simulation
		calendar.  Events are first sorted by occurrence_time.
		If one or more events have the same occurrence_time then
		self.method_comp is used to sort those events.
		'''
		if self.occurrence_time < other.occurrence_time:
			return -1
		if self.occurrence_time > other.occurrence_time:
			return 1
			
		# At this point occurence_time is equal, so we need to 
		# differentiate the events based on the method called
		return self.method_comp(self.method, other.method)
	
	def method_comp(self, method_one, method_two):
		'''Use the ordering defined in the EVENT_METHODS dictionary to
		order two events that have the same occurrence_time.
		'''
		assert (method_one in self.EVENT_METHODS) and (method_two in self.EVENT_METHODS), \
			'One of %s or %s has not been defined in EVENT_METHODS\n' % \
			(method_one, method_two)
			
		if self.EVENT_METHODS[method_one] < self.EVENT_METHODS[method_two]: return -1
		if self.EVENT_METHODS[method_one] > self.EVENT_METHODS[method_two]: return 1
		return 0
	
	def handle_event(self):
		'''Execute object.method(args) at occurrence_time.
		'''
		getattr(self.object, self.method)(*self.args)
