#python 3

"""
	O.S. Process Scheduling Simulation
"""

#CPU States
PROCESS_COMPLETE = 1
FREE_CPU = 0
CPU_BUSY = -1
ERROR = -3

#Scheduling Alogrithms
SJF = 0

# System Clock
class System_Clock():
	time = 0
	def __init__(self):			self.reset()
	def reset(self):			self.time = 0
	def tick(self,t): 			self.time += t
	def get_time(self): 		return self.time

# Process Simulator
class Process_Simulator():
	process_queue = []
	def __init__(self):		self.process_queue = []

	def load_processes_csv_file(self,fname):
		#load processes from csv file into process queue
		with open(fname) as f:
			data = f.readlines()

		data = [x.strip() for x in data]
		for p in data:
			process_attributes = p.split(',')
			PCB = {
				"PID" : int(process_attributes[0]),
				"Priority" : int(process_attributes[3]),
				"time_remaining" : int(process_attributes[2]),
				"time_waiting" : 0,
				"start_time" : -1,
				"end_time" : -1,
				"arriavl_time" : int(process_attributes[1]),
				"burst_time" : int(process_attributes[2]),
			}
			self.process_queue.append(PCB)

	def get_incomming_processes(self, system_time):
		#return processes whose arrival time matches the system time
		incomming_processes = []
		for p in self.process_queue:
			if p["arriavl_time"] == system_time:
				incomming_processes.append(p)
				#self.process_queue.remove(p)

		for p in incomming_processes:
			self.process_queue.remove(p)

		return incomming_processes

	def number_remmaining(self):
		return len(self.process_queue)

class Queue():
	queue = []

	def __init__(self): 	self.queue = []
	def add(self, item):	self.queue.append(item)
	def remove(self):
		new_queue = []
		for i in range(1, len(self.queue)):
			new_queue.append(self.queue[i])
		self.queue = new_queue
	#def add_with_priority(self, item):

	def remove_by_pid(self, PID):
		new_queue = []
		for i in range(0, len(self.queue)):
			if self.queue[i]["PID"] != PID:
				new_queue.append(self.queue[i])
		self.queue = new_queue

	def get_queue(self):		return self.queue

class CPU():
	def __init__(self):
		self.process = []
		self.qval = -1

	def process_change(self, system_time, new_process, qval):

		#if process is not complete need to save the state and shit
		old_process = None
		if len(self.process) > 0:
			old_process = self.process.pop()
		self.process.append(new_process)
		self.qval = qval

		# clean way to do this with mulitple start and stop times
		self.process[0]["start_time"] = system_time

		return old_process

	def execute(self, system_time):
		#completed_processes = []

		"""
		#tmp print
		print ("EXECUTE CPU")
		print ( "--> CPU STATE:" + str(self.state()) )
		if (len(self.process) > 0):
			print ( "--> CURRENT PROCESS:" + str(self.process[0]["PID"]) )
		#tmp print
		"""


		if self.state() == CPU_BUSY:
			self.qval = self.qval -1
			self.process[0]["time_remaining"] = self.process[0]["time_remaining"] -1

		if self.state() == PROCESS_COMPLETE:
			self.process[0]["end_time"] = system_time
			#completed_processes.append(self.process[0])
			#self.process = []
			print ("PROCESS_COMPLETE")

		if self.state() == FREE_CPU:	pass
		if self.state() == ERROR:	print ("CPU Error")

		#return completed_processes

	def get_process(self):
		r = self.process[0]
		self.process = []
		#change state?
		return r

	def state(self):

		#process completed and ready to be returned
		if (len(self.process) > 0) and (self.qval < 1):
			return PROCESS_COMPLETE

		#nothing in cpu
		if len(self.process) < 1:
			return FREE_CPU

		if self.qval > 0:
			return CPU_BUSY

		else: return ERROR

	def current_process_details(self):
		return self.process


# OS
class OS():

	def shortest_job_first(self):

		#find shortest job in ready queue
		jobs = self.ready_queue.get_queue()

		if len(jobs) > 0:
			shortest_job = jobs[0]
			for j in jobs:
				if j["burst_time"] < shortest_job["burst_time"]:
					shortest_job = j

			if self.cpu.state() == PROCESS_COMPLETE:
				self.completed_queue.add(self.cpu.get_process())

			if self.cpu.state() == FREE_CPU :
				#remove by pid
				self.ready_queue.remove_by_pid(shortest_job["PID"])
				self.cpu.process_change(self.clock.get_time(), shortest_job, shortest_job["burst_time"])

		if self.cpu.state() == CPU_BUSY:
			self.cpu.execute(self.clock.get_time())

		#for last remaining process stuck in cpu hacky
		if self.cpu.state() == PROCESS_COMPLETE:
			self.completed_queue.add(self.cpu.get_process())


	def set_type(self, type):	
		self.type = type

	def execute(self):
		self.scheduling_algorithms[self.type]()

	def run(self):
		t = 1
		self.clock.reset()

		#main loop
		running = True
		while running:

			#add incomming processes to ready_queue
			incomming_processes = self.ps.get_incomming_processes(self.clock.get_time())
			for p in incomming_processes:	
				self.ready_queue.add(p)

			self.execute()

			#update waiting times in ready queue
			#time in ques
			#self.ready_queue.update_wait_times(t)

			self.clock.tick(t)

			#print (self.cpu.state())
			if self.ps.number_remmaining() == 0 and len(self.ready_queue.get_queue()) == 0 and self.cpu.state() == FREE_CPU:
				running = False

			#tmp
			print (self.clock.get_time())


		#print out results
		print ("Processes Complete")
		#print (len(self.completed_queue.get_queue()))
		for p in self.completed_queue.get_queue():
			print (p)


	def __init__(self, type, fname):
		self.ready_queue = Queue()
		self.completed_queue = Queue()
		self.cpu = CPU()

		#schedular
		self.scheduling_algorithms = {SJF : self.shortest_job_first}
		self.set_type(type)

		#process simulator
		self.ps = Process_Simulator()
		self.ps.load_processes_csv_file(fname)

		#clock
		self.clock = System_Clock()

		#run
		self.run()



os = OS(0, "pex.txt")

