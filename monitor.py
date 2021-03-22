#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: iKosm

import os
import subprocess
import re
import shutil

statistics = {}
matcher = re.compile("\d+")


def cpu_monitor_count(do_return: bool):
    # Get Physical & Logical CPU Count
    cpu_count = os.cpu_count()

    statistics["cpu_count"] = cpu_count

    if do_return:
        return cpu_count


def cpu_monitor_avg(do_return: bool):
    # Load average
    # Average system load calculated over 1, 5, and 15 minutes.
    # We will average out over a period of 15 minutes. Can be changed later if desired.

    # Calculate load average | calculated into percentage
    cpu_load = [x / os.cpu_count() * 100 for x in os.getloadavg()][-1]

    statistics["cpu_load"] = cpu_load

    if do_return:
        return cpu_load


def ram_monitor(do_return: bool):
    total_ram = subprocess.run(["sysctl", "hw.memsize"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    vm = subprocess.Popen(["vm_stat"], stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    vm_lines = vm.split("\n")

    wired_mem = (int(matcher.search(vm_lines[6]).group()) * 4096) / 1024 ** 3
    free_mem = (int(matcher.search(vm_lines[1]).group()) * 4096) / 1024 ** 3
    active_mem = (int(matcher.search(vm_lines[2]).group()) * 4096) / 1024 ** 3
    inactive_mem = (int(matcher.search(vm_lines[3]).group()) * 4096) / 1024 ** 3

    # Currently used memory = wired_mem + active_mem + inactive_mem

    statistics["ram"] = dict(
        {
            "total_ram": int(matcher.search(total_ram).group()) / 1024 ** 3,
            "used_ram": round(wired_mem + active_mem + inactive_mem, 2),
        }
    )

    if do_return:
        return statistics.get("ram")


def disk_monitor(do_return: bool):
    top_command = subprocess.run(["top", "-1 1", "-n 0"], stdout=subprocess.PIPE).stdout.decode("utf-8")

    # Disk Usage
    # Get total disk size, used disk space, and free space

    total, used, free = shutil.disk_usage("/")

    # Number of Read & Write operations
    # The operation read will return as follows:
    # 'Disks: XXXXXX/xxG read, XXXX/xxG written.'

    read_written = top_command[9].split(":")[1].split(",")
    read = read_written[0].split(" ")[1]
    written = read_written[1].split(" ")[1]

    statistics["disk"] = dict(
        {
            "total_disk_space": round(total / 1024 ** 3, 1),
            "used_disk_space": round(used / 1024 ** 3, 1),
            "free_disk_space": round(free / 1024 ** 3, 1),
            "read_write": {"read": read, "written": written},
        }
    )

    if do_return:
        return statistics.get("disk")


def network_monitor(do_return: bool):
    # We will ping Google servers at an interval of roughly 5 seconds, for 5 times.
    # This will record the min response time, average response time, and the max response time.

    ping_result = (
        subprocess.run(["ping", "-i 5", "-c 5", "google.com"], stdout=subprocess.PIPE)
        .stdout.decode("utf-8")
        .split("\n")
    )

    min_ping, avg_ping, max_ping = ping_result[-2].split("=")[1].split("/")[:3]
    statistics["network_latency"] = dict(
        {
            "min_ping": min_ping.strip(),
            "avg_ping": avg_ping.strip(),
            "max_ping": max_ping.strip(),
        }
    )

    if do_return:
        return statistics.get("network_latency")


def return_stats():
    # Function dedicated to purely calling, displaying, and saving monitor statistics.
    cpu_monitor_count(False)
    cpu_monitor_avg(False)
    ram_monitor(False)
    disk_monitor(False)
    network_monitor(False)

    return statistics
