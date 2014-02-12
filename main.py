import event as ev
import numpy.random as npr
import player
import sim_engine
##

PRIORITY_QUEUING= False

TOTAL_GOLFERS= 50

class GeneratePlayer():
	def __init__(self):
		self.num_arrived= 0
		self.log_label= 'Gen Player'

	def player_arrives(self, sim_cal, sim_time, holes):
		'''Generates a new golfer, and then schedules a new golfer
		arrival with an interarrival time that is exponentially
		distributed with mean 10 units.  A maximum of TOTAL_GOLFERS
		golfers will be generated.
		'''
		self.num_arrived += 1
		golfer_seed= npr.randint(0, 100000000)
		golfer= player.Player(self.num_arrived, sim_time.time, golfer_seed)
		sim_cal.add_event(ev.Event(golfer, 'go_to_hole',
									[sim_cal, sim_time, holes],
									sim_time.time))
									
		if (self.num_arrived < TOTAL_GOLFERS):
			time_to_next= sim_time.time + npr.exponential(10)
			sim_cal.add_event(ev.Event(self, 'player_arrives',
										[sim_cal, sim_time, holes],
										time_to_next))
	
if __name__ == "__main__":
	## Set seed and initialize variable etc needed for the simulation
	npr.seed(200)
	cal= sim_engine.SimulationCalendar()
	time= sim_engine.SimulationTime()
	holes= [[], [], [], [], [], [], [], [], [], []]
	gen= GeneratePlayer()
	
	## Add the first player to the system
	gen.player_arrives(cal, time, holes)

	## Run simulation
	while cal.calendar:
		cal.handle_event(time)	

	## Write data to file for analysis
	data= open('player_data.txt', 'w')
	data.write('ID\tType\tArr. Time\tH1_Wait\tH2_Wait\tH3_Wait\tH4_Wait\tH5_Wait' \
				'\tH6_Wait\tH7_Wait\tH8_Wait\tH9_Wait\tH1_Play\tH2_Play\tH3_Play' \
				'\tH4_Play\tH5_Play\tH6_Play\tH7_Play\tH8_Play\tH9_Play\n')
	for plyr in holes[9]:
		data.write('%s\t' % plyr.id)
		data.write('%s\t' % plyr.type)
		data.write('%s\t' % plyr.arrival_time)
		for wait in plyr.wait_time:
			data.write('%f\t' % wait)
		for play in plyr.play_time:
			data.write('%f\t' % play)
		data.write('\n')
		
	data.close()
	