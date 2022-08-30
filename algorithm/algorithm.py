# This file is part of the ElastiSim software.
#
# Copyright (c) 2022, Technical University of Darmstadt, Germany
#
# This software may be modified and distributed under the terms of the 3-Clause
# BSD License. See the LICENSE file in the base directory for details.

from elastisim_python import JobState, JobType, NodeState, pass_algorithm


def schedule(jobs, nodes, system):
    time = system['time']

    pending_jobs = [job for job in jobs if job.state == JobState.PENDING]
    running_jobs = [job for job in jobs if job.state == JobState.RUNNING]
    reconfiguring_jobs = [job for job in jobs if job.state == JobState.PENDING_RECONFIGURATION]
    completed_jobs = [job for job in jobs if job.state == JobState.COMPLETED]
    killed_jobs = [job for job in jobs if job.state == JobState.KILLED]

    free_nodes = [node for node in nodes if node.state == NodeState.FREE]
    allocated_nodes = [node for node in nodes if node.state == NodeState.ALLOCATED]
    reserved_nodes = [node for node in nodes if node.state == NodeState.RESERVED]

    for job in jobs:
        if (job.type == JobType.MOLDABLE or job.type == JobType.MALLEABLE) and job.state == JobState.PENDING:
            for i in range(job.num_nodes_max, job.num_nodes_min - 1, -1):
                if i <= len(free_nodes):
                    job.assign(free_nodes[:i])
                    del free_nodes[:i]
                    job.assign_num_gpus_per_node(job.num_gpus_per_node_max)
                    break
        elif job.type == JobType.MALLEABLE and job.state == JobState.RUNNING:
            num_assigned_nodes = len(job.assigned_nodes)
            if num_assigned_nodes < job.num_nodes_max:
                for i in range(job.num_nodes_max - num_assigned_nodes, 0, -1):
                    if i <= len(free_nodes):
                        job.assign(free_nodes[:i])
                        del free_nodes[:i]
                        job.assign_num_gpus_per_node(job.num_gpus_per_node_max)
                        break
        elif job.type == JobType.RIGID and job.state == JobState.PENDING:
            if job.num_nodes <= len(free_nodes):
                job.assign(free_nodes[:job.num_nodes])
                del free_nodes[:job.num_nodes]


if __name__ == '__main__':
    url = 'ipc:///tmp/elastisim.ipc'
    pass_algorithm(schedule, url)
