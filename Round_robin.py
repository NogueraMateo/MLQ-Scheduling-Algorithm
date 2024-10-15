from Pcb import PCB
from process import Process

class ProcessExpropiatedException(Exception):
    pass


class ProcessFinishedException(Exception):
    pass


class RoundRobin:

    """
    Implementation of the Round Robin (RR) scheduling algorithm.
    This algorithm executes processes in time slices (quantum) and switches between processes after each slice.
    """

    def __init__(self, quantum: int, processes: list[Process], time: int = 0):
        """
        Initializes the Round Robin simulator with a list of processes, quantum time, and initial simulation time.
        
        :param quantum: The time slice (quantum) for each process before it is preempted.
        :param processes: List of ready processes to be executed.
        :param time: The initial simulation time.
        """
        self.__quantum: int = quantum
        self.__time: int = time 
        self.__initial_time: int = time
        self.__queue: list[Process] = processes
        self.__current_process_started: int = 0
        self.__current_process_index: int = 0

    
    def start_processing(self):
        """
        Starts processing the ready queue using the Round Robin algorithm.
        Processes are executed for a time slice (quantum) before being preempted.
        """
        self.__order_queue()
        next_process = self.__next_process()

        # Continue processing until no processes are left
        while next_process is not None:

            try:
                
                self.__excecute_process(next_process)

            except ProcessExpropiatedException:
                next_process = self.__next_process()
                

    def get_time(self) -> int:
        """
        Returns the current simulation time after processing the queue.

        :return: The current simulation time.
        """
        return self.__time


    def __excecute_process(self, p: Process) -> None:
        """
        Executes a given process for a quantum. If the process finishes before the quantum ends,
        it is marked as done, otherwise it is preempted.
        
        :param p: The process to execute.
        """
        self.__current_process_started = self.__time
        self.__current_process_index = self.__queue.index(p)
        remaining_time = self.__state_restore(p)
        
        for i in range(self.__quantum):
            
            self.__time += 1
            remaining_time -= 1

            if remaining_time == 0:
                self.__state_save(p)
                self.__mark_process_done(p)
                raise ProcessExpropiatedException

            if i == self.__quantum - 1:
                self.__state_save(p)
                raise ProcessExpropiatedException


    def __next_process(self) -> Process:
        """
        Finds and returns the next process to execute. If all processes have been executed,
        it returns None.
        
        :return: The next process to execute, or None if no more processes are left.
        """
        try:
            if self.__time == self.__initial_time:
                return self.__queue[0]

            for i in range(len(self.__queue) - self.__current_process_index + 1):
                p = self.__queue[self.__current_process_index + i +1]
                if not p.get_pcb().is_done():
                    return p

            raise IndexError        
        except IndexError:
            for p in self.__queue:
                if not p.get_pcb().is_done():
                    return p
                continue
        
        return None
    
    
    def __order_queue(self) -> None:
        """
        Orders the processes in the queue based on their arrival time (AT).
        If arrival times are the same, it orders by process tag.
        """
        if self.__queue[-1].get_tag().startswith("p"):
            self.__queue.sort(key= lambda p: (p.get_pcb().get_at(), int(p.get_tag()[1:])))
        else:
            self.__queue.sort(key= lambda p: (p.get_pcb().get_at(), p.get_tag()))

    
    def __state_save(self, p: Process) -> None:
        """
        Saves the current state of the process before it is preempted.
        
        :param p: The process whose state is being saved.
        """
        pcb = p.get_pcb()
        time_excecuted = self.__time - self.__current_process_started
        pcb.set_et(self.__time)
        pcb.set_te(pcb.get_te() + time_excecuted)

        # Set response time if this is the first execution
        if pcb.get_rt() < 0:
            pcb.set_rt(self.__current_process_started)

    
    def __state_restore(self, p: Process) -> None:
        """
        Restores the remaining burst time of the process to continue execution.
        
        :param p: The process whose state is being restored.
        :return: The remaining burst time for the process.
        """
        pcb = p.get_pcb()
        return pcb.get_bt() - pcb.get_te()


    def __mark_process_done(self, p: Process) -> None:
        """
        Marks a process as done and calculates its final metrics (Completion Time, Waiting Time, Turnaround Time).
        
        :param p: The process to be marked as done.
        """
        pcb = p.get_pcb()
        pcb.set_done()

        pcb.set_ct(self.__time)
        pcb.set_wt(pcb.get_ct() - pcb.get_at() - pcb.get_bt())
        pcb.set_tat(pcb.get_ct() - pcb.get_at())
    

    def __calculate_metrics(self):
        """
        Placeholder for calculating overall metrics (if needed for average statistics).
        """
        pass
    

    def get_metrics(self):
        """
        Prints the information and metrics for all processes in the queue.
        """
        for p in self.__queue:
            print(p.get_info())
