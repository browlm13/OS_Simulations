#python 3

"""
	Queue Data Structure

	add() // to tail defualt, or index
	remove() // head by defualt, or pid

"""

#
#	Process
#

class Process():

	def __init__(self, id, arrival_time, burst_time, priority):
		self.pid = id
		self.arrival_time = arrival_time
		self.burst_time = burst_time
		self.priority = priority
		self.time_remaining = burst_time

	def step(self):
		if (self.time_remaining <= 1):
			return False

		self.time_remaining -= 1
		return True

	def __getitem__(self, tag):
		if tag == 'pid':return self.pid
		if tag == 'arrival_time':return self.arrival_time
		if tag == 'burst_time':return self.burst_time
		if tag == 'priority':return self.priority
		if tag == 'time_remaining':return self.time_remaining

	def __repr__(self):
		s = "pid: %d, \t at: %d, \t bt: %d, \t p: %d, \t tr: %d\n" % (self.pid, self.arrival_time, self.burst_time, self.priority, self.time_remaining)
		return s

	def reset(self):
		self.time_remaining = self.burst_time


#
#	Processes Queue
#

node = lambda p, next: {'process':p, 'next':next}

class queue():

	def __init__(self):
		self.head, self.tail = None, None

	def add(self, process):
		n = node(process, None)

		if self.head == None:
			self.head, self.tail = n, n

		else:
			self.tail['next'] = n
			self.tail = n

	def remove(self, pid=None):

		if self.head != None:

			#search by process id
			if pid != None:
				last, cur = self.head, self.head
				process = None

				while cur != None:
					if cur['process'].pid == pid:
						process = cur['process']
						if last == cur:
							self.head = cur['next']
						elif cur['next'] == None:
							last['next'] = None
						elif cur['next'] != None:
							last['next'] = cur['next']
						break

						#return cur['process']

					last = cur
					cur = cur['next']

				#fix tail
				if self.head != None:
					cur = self.head
					while cur['next'] != None:
						cur = cur['next']

					self.tail = cur 
				else:
					self.tail = self.head

				assert process != None
				return process

			# no pid arg
			n = self.head
			self.head = n['next']
			return n['process']

	def __getitem__(self, index):
		assert self.head != None
		cur = self.head
		for i in range(index):
			cur = cur['next']
			assert cur != None

		return cur['process']

	def __contains__(self, pid):
		if self.head != None:
			#loop and search
			cur = self.head
			while cur != self.tail:
				if cur['process'].pid == pid:
					return True
				cur = cur['next']

			return False

	def __len__(self):
		if self.head == None:
			return 0
		count = 1
		cur = self.head
		while (cur != self.tail) and (cur != None):
			cur = cur['next']
			count += 1
		return count

	def __repr__(self):

		s = ""
		for i in range(len(self)):
			p = self[i]
			s += str(p)#"\npid: %d, \tarrival_time: %d, \tburst_time: %d, \tpriority: %d" % (p.pid, p.arrival_time, p.burst_time, p.priority)
		return s


	def reversed(self):
		reversed_queue = queue()

		for i in range(len(self)-1,-1,-1):
			reversed_queue.add(self[i])

		return reversed_queue


	def sort(self, attribute, descending=False):
			q = self.__copy__()
			length = len(q)

			sorted_queue = queue()
			while len(sorted_queue) < length:
				minimum = q[0]
				for i in range(len(q)):
					if q[i][attribute] < minimum[attribute]:
						minimum = q[i]
				q.remove(minimum['pid'])
				sorted_queue.add(minimum)

			if descending == True:
				return sorted_queue.reversed() 

			return sorted_queue	

	def __copy__(self):
	  cpy = type(self)()

	  if len(self) == 0:
	  	return cpy

	  for i in range(len(self)):
	  	cpy.add(self[i])

	  return cpy


#Scheduling Alogrithms
FCFS = 0
SJF = 1
NPP = 2
RR = 3

scheduling_algorithms = {
	FCFS : "First Come First Serve",
	SJF : "Shortest Job First",
	NPP : "Non-Premptive Priority",
	RR : "Round Robin",
}

scheduling_algorithm_quantoms = {
	FCFS : None,
	SJF : None,
	NPP : None,
	RR : 5,
}

class STS():

	def shortest_job_first(self):
		#sort ready queue
		self.ready_queue = self.ready_queue.sort('time_remaining')

		#choose quantom
		return self.ready_queue[0].burst_time + 1

	def non_preemptive_priority(self):
		#sort ready queue
		self.ready_queue = self.ready_queue.sort('priority')

		#choose quantom
		return self.ready_queue[0].burst_time + 1


	def first_come_first_serve(self):
		#already sorted

		#choose quantom
		return self.ready_queue[0].burst_time + 1

	def round_robin(self):
		#already sorted

		#choose quantom
		return self.quantom



	def __init__(self, type, quantom=None):
		self.ready_queue = queue()

		#schedular
		self.scheduling_algorithms = {
										SJF : self.shortest_job_first,

										NPP : self.non_preemptive_priority,

										FCFS : self.first_come_first_serve,

										RR : self.round_robin

										}
		self.type = type
		self.quantom = quantom


	def new_jobs(self, process_list):
		for p in process_list:
			self.ready_queue.add(p)

	def dispatcher(self, process=None):
		quantom = None

		if process != None:
			self.ready_queue.add(process)

		if len(self.ready_queue) > 0:
			#sort
			quantom = self.scheduling_algorithms[self.type]()

			# add terminal process to end no matter what if there
			try:
				terminal_process = self.ready_queue.remove(-666)
				self.ready_queue.add(terminal_process)
			except: pass

			return self.ready_queue.remove(), quantom

		return None, None

class CPU():

	def __init__(self, STS):
		self.STS = STS
		self.process = None
		self.quantom = None

	def tick(self):

		if self.process == None:
			self.process, self.quantom = self.STS.dispatcher()

		if self.process != None:

			#check for terminal process
			if self.process.pid == -666:
				return False

			#execute process
			#print ("EXECUTE: %d" % self.process.pid)

			if not self.process.step():

				#print ("TERMINATED: %d" % self.process.pid)
				#process ended
				self.process, self.quantom = self.STS.dispatcher()

				#if self.process != None:
				#	#print ("NEW PROCESS: %d" % self.process.pid)
				#	#print ("QUANTOM: %d" % self.quantom)

		if self.process != None:
			self.quantom -= 1
			if self.quantom <= 0:
				#print ("QUANTOM REACHED, PID: %d"  % self.process.pid)
				self.process, self.quantom = self.STS.dispatcher(self.process)
				#print ("NEW PROCESS: %d" % self.process.pid)
				#print ("QUANTOM: %d" % self.quantom)

		return True

	def pid(self):
		if self.process != None:
			return self.process.pid

class LTS():

	def _create_track(self):
		sorted_job_pool = self.job_pool.sort('arrival_time')

		waiting_ticks = [0]
		process_batches = []

		i = 0
		while i < (len(sorted_job_pool)):
			time = sorted_job_pool[i].arrival_time
			next_wait_time = time - waiting_ticks[-1]
			waiting_ticks.append(next_wait_time)
			batch = []
			j = i
	
			inbounds = True
			while inbounds and (sorted_job_pool[j].arrival_time == time):
				batch.append(sorted_job_pool[j].pid)
				j += 1
				if j >= len(sorted_job_pool):
					inbounds = False	

			i = j
			process_batches.append(batch)
		waiting_ticks.pop(0)

		#add -666 process to job pool and end of process batches
		terminal_process = Process(-666,666,666,666)
		self.job_pool.add(terminal_process)
		process_batches[-1].append(-666)

		self.process_batches = process_batches
		self.waiting_ticks = waiting_ticks

	def __init__(self, job_pool, STS):
		self.job_pool = job_pool.__copy__()
		self.STS = STS

		self._create_track()

		#print (self.waiting_ticks)
		#print (self.process_batches)
		#print (self.job_pool)


	def tick(self):

		if len(self.waiting_ticks) > 0:
			if self.waiting_ticks[0] == 0:
				self.waiting_ticks.pop(0)

				#new jobs
				process_list = []
				for i in self.process_batches[0]:
					process_list.append(self.job_pool.remove(i))

				self.STS.new_jobs(process_list)
		
				self.process_batches.pop(0)
			else:
				self.waiting_ticks[0] -= 1


class Gnatt():

	def __init__(self, CPU):
		self.CPU = CPU
		self.gnatt = []

	def tick(self):
		pid = self.CPU.pid()
		if pid != None:
			self.gnatt.append(pid)

	def export(self, context_switch_penatly=None):

		polish = []
		current_process = self.gnatt[0]
		count = 1
		for i in range(len(self.gnatt)-1):
			if self.gnatt[i] == current_process:
				count += 1
			else:
				block = [current_process, count]
				polish.append(block)
				current_process = self.gnatt[i]
				count = 1
		return polish

def wait_time(gnatt, pid):
	t = 0

	#find last occurence of pid
	last_occurence_index = 0
	for i in range(len(gnatt)):
		if gnatt[i][0] == pid:
			last_occurence_index = i

	#until last occurance of pid
	for i in range(last_occurence_index):
		if gnatt[i][0] != pid:
			t += gnatt[i][1]
	return t

def average_wait_time(gnatt):
	#find number of unique processes by gnatt[][0]
	unique_process_ids = []
	for i in range(len(gnatt)):
		if gnatt[i][0] not in unique_process_ids:
			unique_process_ids.append(gnatt[i][0])

	total_wait_times = 0
	for pid in unique_process_ids:
		total_wait_times += wait_time(gnatt, pid)

	return total_wait_times/len(unique_process_ids)

def turnaround_time(gnatt, pid):
	t = 0

	#find last occurence of pid
	last_occurence_index = 0
	for i in range(len(gnatt)):
		if gnatt[i][0] == pid:
			last_occurence_index = i

	#sum total execution time until and including last occurence
	for i in range(last_occurence_index + 1):
		t += gnatt[i][1]

	return t

def average_turnaround_time(gnatt):
	#find number of unique processes by gnatt[][0]
	unique_process_ids = []
	for i in range(len(gnatt)):
		if gnatt[i][0] not in unique_process_ids:
			unique_process_ids.append(gnatt[i][0])

	total_turnaround_times = 0
	for pid in unique_process_ids:
		total_turnaround_times += turnaround_time(gnatt, pid)

	return total_turnaround_times/len(unique_process_ids)


"""
# from file
def load_processes_csv_file(fname):

	job_queue = queue()

	#load processes from csv file into process queue
	with open(fname) as f:
		data = f.readlines()

	data = [x.strip() for x in data]
	for p in data:
		process_attributes = p.split(',')
		PCB = {
			"PID" : int(process_attributes[0]),
			"arriavl_time" : int(process_attributes[1]),
			"burst_time" : int(process_attributes[2]),
			"Priority" : int(process_attributes[3]),
		}
		p = Process(PCB['PID'], PCB['arriavl_time'], PCB['burst_time'], PCB['Priority'])
		job_queue.add(p)

	return job_queue.__copy__()

job_pool_master = load_processes_csv_file('pex.txt')
print (job_pool_master)
"""

# random generation
import random

job_pool_master = queue()

num = 20
for i in range(num):
	job_pool_master.add(Process(i+1,random.randint(0,num),random.randint(1,num),random.randint(1,4)))

print (job_pool_master)




for alg in scheduling_algorithms:

	#reset job pool and processes
	job_pool = job_pool_master.__copy__()
	for i in range(len(job_pool)):
		job_pool[i].reset()

	sts = STS(alg, scheduling_algorithm_quantoms[alg])
	lts = LTS(job_pool, sts)
	cpu = CPU(sts)
	gnatt = Gnatt(cpu)

	run = True
	while run:
		lts.tick()
		gnatt.tick()
		run = cpu.tick()

	g = gnatt.export()

	avg_tt = average_turnaround_time(g)
	avg_wt = average_wait_time(g)


	print ("ALG: %s, \tQuantom: %s, \twt: %f, \ttt: %f\n" % ( scheduling_algorithms[alg], str(scheduling_algorithm_quantoms[alg]), avg_wt, avg_tt ) )
