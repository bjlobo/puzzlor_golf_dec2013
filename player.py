import event as ev
import main
import numpy.random as npr
##

class Player(object):
	mpt= {'fast': 5, 'medium': 7, 'slow': 10}
	
	def __init__(self, player_number, arrival_time, seed):
		'''Player class used to track an individual player
		through his round of golf.
		id: unique id equal to the number of the player
			entering the system
		rnd_stream: player specific random stream used to
			generate player type and play times
		type: type of player (fast, medium, slow)
		at_hole: current hole that the player is waiting at
			or playing
		arrival_time: time at which player entered the system,
			used for data analysis
		mean_playing_time: based on the type of player
		wait_time: list used to store the wait time of the
			player at each hole
		play_time: list used to store the play time of the
			player at each hole
		log_label: used for debugging		
		'''
		self.id= player_number
		self.rnd_strm= npr.RandomState(seed)
		self.type= self.determine_type()
		self.at_hole= 0
		self.arrival_time= arrival_time
		self.mean_playing_time= self.mpt[self.type]
		self.wait_time= []
		self.play_time= []
		self.log_label= player_number		
	
	def __str__(self):
		return 'PNum: %s, Type: %s, Hole: %s\n' \
			% (self.log_label, self.type, self.at_hole)

	def determine_type(self):
		'''The player can be any one of the three types
		of player with equal chance.
		'''
		return self.rnd_strm.choice(self.mpt.keys(), 1)[0]
	
	def go_to_hole(self, sim_cal, sim_time, holes):
		'''The player places himself on holes[self.at_hole] list.
		self.wait_time stores the time that waiting begins for 
		this player, and is updated to the actual waiting time
		in 'play_hole'.
		If the hole is empty (i.e. this player is the only one
		on self.at_hole list), the player schedules himself to
		play the hole.
		'''
		holes[self.at_hole].append(self)

		self.wait_time.append(sim_time.time)
		if len(holes[self.at_hole]) == 1:
			sim_cal.add_event(ev.Event(self, 'play_hole',
										[sim_cal, sim_time, holes],
										sim_time.time))
								
	def play_hole(self, sim_cal, sim_time, holes):
		'''The waiting time is updated to the true waiting time.
		An event for the player finishing the hole is scheduled.		
		'''
		self.wait_time[-1]= sim_time.time - self.wait_time[-1]
		self.play_time.append(self.hole_time())

		finish_time= sim_time.time + self.play_time[-1]
		sim_cal.add_event(ev.Event(self, 'finish_hole',
									[sim_cal, sim_time, holes],
									finish_time))
	
	def finish_hole(self, sim_cal, sim_time, holes):
		'''The player removes himself from the list, and moves to
		the next hole (unless he has reached the end of the nine holes).
		A check is made to see if there is someone waiting to play on
		the hole just finished, and if there is the player is scheduled
		to play the hole.  If the priority queuing scheme is being used,
		the list is sorted before the player is picked.
		'''
		holes[self.at_hole].pop(0)

		self.at_hole += 1
		if self.at_hole == 9:
			holes[self.at_hole].append(self)
		else:
			sim_cal.add_event(ev.Event(self, 'go_to_hole',
										[sim_cal, sim_time, holes],
										sim_time.time))

		current_hole= self.at_hole - 1
		if len(holes[current_hole]) > 0:
			if main.PRIORITY_QUEUING:
				holes[current_hole].sort(key= lambda x: x.type)

			next_player= holes[current_hole][0]
			sim_cal.add_event(ev.Event(next_player, 'play_hole',
										[sim_cal, sim_time, holes],
										sim_time.time))		

	def hole_time(self):
		'''Returns the time it takes for the player to play
		the hole.
		'''
		return self.rnd_strm.normal(self.mean_playing_time, 1)
