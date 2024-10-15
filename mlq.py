from process import Process
from Pcb import PCB
from Round_robin import RoundRobin
from fcfs import FCFS

import os

class MLQ:
    """
    Implementation of the Multilevel Queue (MLQ) scheduling algorithm.
    This algorithm manages multiple queues, where each queue can use a different scheduling algorithm.
    """

    def __init__(self, filename: str):
        """
        Initializes the MLQ simulator by reading the input file and initializing the queues and processes.
        
        :param filename: The name of the file containing process information.
        """
        self.__filename: str = filename
        self.__queues : list[list[Process]] = []
        self.__time: int = 0

        self.__read_file(filename)


    def start_processing(self) -> None:
        """
        Starts processing each queue based on its assigned scheduling algorithm.
        Queue 1 uses Round Robin with a quantum of 3.
        Queue 2 uses Round Robin with a quantum of 5.
        Queue 3 uses First Come First Serve (FCFS).
        """
        for i in range(len(self.__queues)):

            if len(self.__queues[i]) > 0:
                if i == 0: 
                    rr3 = RoundRobin(3, self.__queues[i], self.__time)
                    rr3.start_processing()
                    self.__time = rr3.get_time()
                elif i == 1:
                    rr5 = RoundRobin(5, self.__queues[i], self.__time)
                    rr5.start_processing()
                    self.__time = rr5.get_time()
                elif i == 2:
                    fcfs = FCFS(self.__queues[i], self.__time)
                    fcfs.start_processing()
                    self.__time = fcfs.get_time()
                

    def __read_file(self, filename: str) -> None:
        """
        Reads the input file to initialize processes and assign them to their respective queues.
        The file format contains information like process tag, burst time, arrival time, queue, and priority.
        
        :param filename: The name of the file to read process data from.
        """
        processes: list[Process] = []

        # Open and read the file
        with open(f"./pruebas/{filename}", "r") as f:
            lines = f.read().splitlines()
            # Track the highest queue number
            max_queues = 0

            # Process each line, skipping the header lines
            for i in range(len(lines)): 
                # Skip headers
                if i == 0 or i == 1:
                    continue
                
                tag, bt, at, queue, priority = lines[i].split(";")
                at = int(at.strip())
                bt = int(bt.strip())
                queue = int(queue.strip())
                max_queues = queue if queue > max_queues else max_queues
                processes.append(Process(tag, at, bt, priority, queue))

        # Initialize empty lists for each queue
        for i in range(max_queues):
            self.__queues.append([])

        # Add processes to their respective queues
        for p in processes:
            self.__queues[p.get_pcb().get_queue() - 1].append(p)


    def get_metrics(self) -> None:
        """
        Calculates and writes the metrics (Waiting Time, Completion Time, Response Time, Turnaround Time)
        to a file. Each process's metrics are written, followed by the averages for each metric.
        """
        # Construct the output filename based on the input filename
        filename = f"./results/{self.__filename}"
        folder = os.path.dirname(filename)
        if folder:
            os.makedirs(folder, exist_ok=True)

        total_wt, total_ct, total_rt, total_tat = 0, 0, 0, 0
        num_processes = 0

        # Open the output file for writing
        with open(filename, "w") as f:
            f.write("# etiqueta; BT; AT; Q; Pr; WT; CT; RT; TAT\n")

            # Iterate through each queue and each process to calculate and write metrics
            for queue in self.__queues:
                for p in queue:
                    pcb = p.get_pcb()

                    wt = pcb.get_wt()
                    ct = pcb.get_ct()
                    rt = pcb.get_rt()
                    tat = pcb.get_tat()

                    
                    total_wt += wt
                    total_ct += ct
                    total_rt += rt
                    total_tat += tat
                    num_processes += 1

                    # Write process metrics to the output file
                    f.write(f"{p.get_tag()}; {pcb.get_bt()}; {pcb.get_at()}; "
                            f"{pcb.get_queue()}; {pcb.get_priority()}; {wt}; {ct}; {rt}; {tat}\n")

            avg_wt = total_wt / num_processes
            avg_ct = total_ct / num_processes
            avg_rt = total_rt / num_processes
            avg_tat = total_tat / num_processes

            # Write the average metrics at the end of the file
            f.write(f"WT={avg_wt:.2f}; CT={avg_ct:.2f}; RT={avg_rt:.2f}; TAT={avg_tat:.2f};\n")

    
def main():
    filename = "mlq001.txt"
    mlq = MLQ(filename)
    mlq.start_processing()
    print(f"Results saved in ./results/{filename}")
    mlq.get_metrics()

if __name__ == '__main__':
    main()