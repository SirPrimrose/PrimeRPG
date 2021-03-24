#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Snack

import os
import subprocess
import shutil


class Monitor:
    def __init__(self, mon_time: int = None, do_log: bool = None) -> None:
        """
        :param mon_time: Monitor Time | How long, in minutes, shall the system monitor processes
        :param do_log: Do Logging | Will the system save a log, rather than terminating after execution
        """
        self.mon_time = mon_time * 60
        self.do_log = do_log

    def get_sys_proc(self):
        # Create new dictionary / Clean old data
        sys_data = {}

        # Get Physical & Logical CPU Count
        try:
            cpu_count = os.cpu_count()
        except OSError:
            return OSError.strerror

        # Obtain usable CPUs the current process can use.
        try:
            usable_cpu_count = len(os.sched_getaffinity(0))
        except OSError:
            return OSError.strerror

        # Calculated CPU load average over a span of 1, 5, and 15 minutes. [Returns as a percentage]
        cpu_load_avg = [x / cpu_count * 100 for x in os.getloadavg()][-1]

        # Store CPU data into system dictionary
        sys_data["cpu"] = dict(
            {
                "cpu_count": cpu_count,
                "usable_cpu_count": usable_cpu_count,
                "cpu_load_avg": cpu_load_avg,
            }
        )

        # Obtain [Total | Used | Free] system RAM information. [Returns in mB format]
        total_mem, used_mem, free_mem = map(int, os.popen("free -t -m").readlines()[-1].split()[1:])

        # Human readable percentage for accurate RAM usage. [Integer based round method]
        mem_percentage = round((used_mem / total_mem) * 100, 0)

        # Store RAM data into system dictionary
        sys_data["ram"] = dict(
            {
                "total_mem": total_mem,
                "used_mem": used_mem,
                "free_mem": free_mem,
                "mem_percentage": mem_percentage,
            }
        )

        # Low level linux 'TOP' command. Obtains all disk information on system.
        top_command = subprocess.run(["top", "-1 1", "-n 0"], stdout=subprocess.PIPE).stdout.decode("utf-8")

        # Obtain [Total | Used | Free] system DISK information.
        total, used, free = shutil.disk_usage("/")

        # Number of Read & Write operations
        # The operation read will return as follows:
        # 'Disks: XXXXXX/xxG read, XXXX/xxG written.'
        read_written = top_command[9].split(":")[1].split(",")
        read = read_written[0].split(" ")[1]
        written = read_written[1].split(" ")[1]

        # Store DISK data into system dictionary
        sys_data["disk"] = dict(
            {
                "total_disk_space": round(total / 1024 ** 3, 1),
                "used_disk_space": round(used / 1024 ** 3, 1),
                "free_disk_space": round(free / 1024 ** 3, 1),
                "read_write": {"read": read, "written": written},
            }
        )

        # We will ping Google servers at an interval of roughly 5 seconds, for 5 times.
        # This will record the min response time, average response time, and the max response time.
        ping_result = (
            subprocess.run(["ping", "-i 5", "-c 5", "google.com"], stdout=subprocess.PIPE)
            .stdout.decode("utf-8")
            .split("\n")
        )

        # Obtain [Minimum | Average | Maximum] network information from ping_result and parses the data
        min_ping, avg_ping, max_ping = ping_result[-2].split("=")[1].split("/")[:3]

        # Store NETWORK data into system dictionary
        sys_data["network_latency"] = dict(
            {
                "min_ping": min_ping.strip(),
                "avg_ping": avg_ping.strip(),
                "max_ping": max_ping.strip(),
            }
        )

        if self.do_log:
            pass
