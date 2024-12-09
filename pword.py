### Grupo: SO-TI-02
### Aluno 1: André Alexandre (fc62224)
### Aluno 2: Sofian Fathallah (fc62814)
### Aluno 3: Tair Injai (fc62848)

import sys, os, signal, argparse, time
from datetime import datetime
from multiprocessing import Process, current_process, Value, Lock, Queue, Array





def parse_arguments(arg):
    """
    Parses command-line arguments for a parallel word search and count script.
    Requires:
        - `arg` is a list of strings.
        - `arg` should include:
            - `-m` with a value of "c", "l", or "i" (optional, defaults to "c"),
            - `-p` with a positive integer specifying the number of parallel processes (optional, defaults to 1),
            - `-i` with a positive float specifying the time of the interval between the partial results of execution (optional, defaults to 3),
            - `-d` with a non-empty string representing the file to write the partial results (optional, defaults to stdout),
            - `-w` with a non-empty string representing the word to search (required),
            - One or more file paths for the positional `files` argument (required).
    Ensures:
        - Returns a `Namespace` object with attributes:
            - `m` set to the selected mode ("c", "l", or "i"),
            - `p` set to the specified or default number of parallel processes,
            - `i` set to the time of the interval between the partial results of execution,
            - `d` containing the file to write the partial results,
            - `w` containing the word to search,
            - `files` as a list of file paths.
        - Raises an error if any required argument is missing or invalid.
    """

    parser = argparse.ArgumentParser(description="Parallel word search and count")
    parser.add_argument("-m", choices=["c", "l", "i"], default="c", help="Modo de contagem: c (total), l (linhas), i (isolado)")
    parser.add_argument("-p", type=int, default=1, help="Número de processos paralelos")
    parser.add_argument("-i", type=float, default=3, help="Intervalo de tempo dos resultados parciais da execução")
    parser.add_argument("-d", type=str, default=None, help="O ficheiro de destino da emissão dos resultados parciais")
    parser.add_argument("-w", required=True, help="Palavra a ser pesquisada")
    parser.add_argument("files", nargs="+", help="Lista de ficheiros")
    return parser.parse_args(arg)





def controlC(signum, frame):
    global stop_processing
    stop_processing = True
    print("\nWill stop processing!")





def handler(mode, file_results, start_time, ocurrencesV, ocurrencesQ, ocurrencesA, part, first_part):
    def inner_handler(signum, frame):
        partial_results(mode, file_results, start_time, ocurrencesV, ocurrencesQ, ocurrencesA, part, first_part)
    return inner_handler





def count_words(lines, word, mode):
    """
    Counts occurrences of a specified word in a list of text lines based on the selected mode.
    Requires:
        - lines must be a list of strings, each representing a line of text.
        - word must be a non-empty string representing the word to count in `lines`.
        - mode must be one of:"c" (count all occurrences of word in each line), 
         "l" (count lines that contain `word` at least once),"i" (count isolated 
         occurrences of `word` as a distinct word in each line).
    Ensures:
        - Returns an integer, `total_count`, representing the count of `word` 
        occurrences based on the specified `mode`.
    """
        
    total_count = 0
    full_linesL = set()
    full_linesI = 0


    for line in lines:
        if mode == "c":
            total_count += line.count(word)

        elif mode == "l":
            if word in line:
                total_count += 1
                full_linesL.add(line)
                

        elif mode == "i":
            words_in_line = line.split()
            total_count += words_in_line.count(word)
            full_linesI += words_in_line.count(word)


    return total_count, full_linesL, full_linesI





def split_file(filename, num_parts):
    """
    The function takes a file and splits it into 'num_parts' roughly equal parts.
    Ensures: 
        - filename is a non-empty string.
        - num_parts is a positive integer greater than zero.  
    Requires: 
        - A list of parts of file content, where each part is a sub-list of lines.
    """

    with open(filename[0], 'r', encoding='utf-8') as file:
        lines = file.readlines()
    size = len(lines) // num_parts
    return [lines[i*size:(i+1)*size] for i in range(num_parts - 1)] + [lines[(num_parts-1)*size:]]





def partial_results(mode, file_results, start_time, occurrencesV, ocurrencesQ, ocurrencesA, part, first_part):
    """
    This function prints or writes the current state of the program.

    """

    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    elapsed_time = int((time.time() - start_time) * 1e6)

    if mode == "c":
        entry = f"{timestamp} {elapsed_time} {occurrencesV.value} {first_part-part.value} {part.value}\n"
    else:
        entry = f"{timestamp} {elapsed_time} {sum(ocurrencesA)} {first_part-part.value} {part.value}\n"

    if file_results:
        with open(file_results+".log", "a") as file:
            file.write(entry)
    else:
        sys.stdout.write(entry)





def prcs(lines, filename, word, mode, ocurrencesV, mutex, ocurrencesQ, ocurrencesA, part, first_part):
    """
    Process a given list of text lines to count the occurrences of a specified word, 
    and print the result along with process and file information.
    Requires:
        - lines must be a non-empty  string.
        - filename must be a non-empty string .
        - word must be a non-empty string .
        - mode must be 'c','i' or 'l'.
        - ocurrencesV, mutex, ocurrencesQ, ocurrencesA and part  are multiprocessing.Value, Lock, Queue, Array and Value respectively.
        - first_part is a string.
    Ensures:
        - Counts the occurrences of word in lines according to the specified `mode` and updates the multiprocessing variables.
    """
    count = count_words(lines, word, mode)

    if mode == "c":
        countV = count[0]
        mutex.acquire()
        ocurrencesV.value = ocurrencesV.value + countV
        part.value = part.value - 1
        mutex.release()


    elif mode == "l":
        countA = count[0]
        full_lines = count[1]
        ocurrencesQ.put(full_lines)
        mutex.acquire()
        ocurrencesA[first_part-part.value] = countA
        part.value = part.value - 1
        mutex.release()

    else:
        countA = count[0]
        full_lines = count[2]
        ocurrencesQ.put(full_lines)
        mutex.acquire()
        ocurrencesA[first_part-part.value] = countA
        part.value = part.value - 1
        mutex.release()





    # elif mode == "i":
    #     with lock:
    #         shared_count.value += count

    # Update counters for processed and remaining
    # with lock:
    #     processed_count.value += 1
    #     remaining_count.value -= 1





def distribute(files, word, mode, num_processes, time_results, file_results, start_time, ocurrencesV, mutex, ocurrencesQ, ocurrencesA):
    """
    Distributes file processing tasks across multiple processes for a word count operation.
    Requires:
        - `files` is a list of strings, each representing a valid file path, with at least one file specified.
        - `word` is a non-empty string that represents the word to search and count within the files.
        - `mode` is a string and must be one of:
            - "c" for counting all occurrences of `word` in each line,
            - "l" for counting lines containing `word` at least once,
            - "i" for counting isolated occurrences of `word` as a distinct word in each line.
        - `num_processes` is a positive integer, specifying the number of processes for parallel execution,
        - `time_results` with a positive float specifying the time of the interval between the partial results of execution,
        - `file_results` with a non-empty string representing the file to write the partial results(optional, defaults to stdout),

    Ensures:
        - Distributes the task of counting `word` occurrences across up to `num_processes` parallel processes.
        - If only one file is provided:
            - Splits the file into `num_processes` parts using `split_file` and assigns each part to a separate process.
        - If multiple files are provided:
            - Divides the files evenly among `num_processes`, assigning a subset of files to each process.
        - Each process executes `prcs` on its assigned file parts or group of files, counting `word` based on the specified `mode`.
        - All processes are started and joined, ensuring completion before the function exits.
    """

    global stop_processing
    stop_processing = False
    signal.signal(signal.SIGINT, controlC)

    processes = []

    global sumQ
    sumQ = 0
    global totalQ
    totalQ = []

    if len(files) == 1:
        filename = files
        file_parts = split_file(filename, num_processes)
        first_part = len(file_parts)
        part = Value("i", first_part)
        for i, lines in enumerate(file_parts):
            if stop_processing == False:
                process = Process(target=prcs, args=(lines, filename, word, mode, ocurrencesV, mutex, ocurrencesQ, ocurrencesA, part, first_part), name=i+1)
                processes.append(process)
                process.start()

                if mode == "l" or mode == "i":
                    totalQ.append(ocurrencesQ.get())

            else:
                break

    else: 
        file_groups = [files[i::num_processes] for i in range(num_processes)]
        first_part = len(file_groups)
        part = Value("i", first_part)
        for i, file_group in enumerate(file_groups):
            if stop_processing == False:
                lines = []
                for filename in file_group:
                    with open(filename, 'r', encoding='utf-8') as file:
                        lines.extend(file.readlines())
                process = Process(target=prcs, args=(lines, ', '.join(file_group), word, mode, ocurrencesV, mutex, ocurrencesQ, ocurrencesA, part, first_part), name=i+1)
                processes.append(process)
                process.start()

                if mode == "l" or mode == "i":
                    totalQ.append(ocurrencesQ.get())

            else:
                break


    if mode == "l":
        for i in totalQ:
            sumQ = sumQ + len(i)

    if mode == "i":
        for i in totalQ:
            sumQ = sumQ + i


    signal.signal(signal.SIGALRM, handler(mode, file_results, start_time, ocurrencesV, ocurrencesQ, ocurrencesA, part, first_part))
    signal.setitimer(signal.ITIMER_REAL, 0.000001, time_results)


    for p in processes:
        p.join()

    return





def main(args):
    """
    Main function to parse command-line arguments and initiate parallel word search and count tasks.
    Requires:
        - `args` is a list of strings representing command-line arguments, typically from `sys.argv[1:]`.
    Ensures:
        - Parses `args` into an `argparse.Namespace` and extracts:
            - `files`: list of file paths to be processed,
            - `word`: the word to be counted in `files`,
            - `mode`: the counting mode,
            - `num_processes`: the number of processes for parallel execution,
            - `time_results`: the time interval between the results,
            - `file_results`: the file to write the results.

        - Prints program name ("Programa: pword.py") and parsed arguments for confirmation.
    """
        
    args = parse_arguments(args)
    files = args.files
    word = args.w
    mode = args.m
    num_processes = args.p
    time_results = args.i
    file_results = args.d

    start_time = time.time()

    print('Programa: pword.py')
    print('Argumentos: ', args, "\n")


    if len(files) < num_processes and len(files)!=1:
        num_processes = len(files)


    if mode == "c":
        ocurrencesV = Value("i", 0)
        mutex = Lock()

        distribute(files, word, mode, num_processes, time_results, file_results, start_time, ocurrencesV, mutex, None, None)
        sys.stdout.write(f"Total occurrences: {ocurrencesV.value}\n")

    elif mode == "l":
        ocurrencesQ = Queue()
        ocurrencesA = Array("i", num_processes)
        mutex = Lock()
        distribute(files, word, mode, num_processes, time_results, file_results, start_time, None, mutex, ocurrencesQ, ocurrencesA)
        sys.stdout.write(f"Total lines (Array): {sum(ocurrencesA)}")
        sys.stdout.write(f"Total lines (Queue): {sumQ}")


    else:
        ocurrencesQ = Queue()
        ocurrencesA = Array("i", num_processes)
        mutex = Lock()
        distribute(files, word, mode, num_processes, time_results, file_results, start_time, None, mutex, ocurrencesQ, ocurrencesA)
        sys.stdout.write(f"Total isolated occurrences (Array): {sum(ocurrencesA)}")
        sys.stdout.write(f"Total isolated occurrences (Queue): {sumQ}")





if __name__ == "__main__":
    main(sys.argv[1:])
