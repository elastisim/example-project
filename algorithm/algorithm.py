# This file is part of the ElastiSim software.
#
# Copyright (c) 2022, Technical University of Darmstadt, Germany
#
# This software may be modified and distributed under the terms of the 3-Clause
# BSD License. See the LICENSE file in the base directory for details.
from typing import Any

from elastisim_python import JobState, JobType, NodeState, pass_algorithm, Job, Node


def schedule(jobs: list[Job], nodes: list[Node], system: dict[str, Any]) -> None:
    time = system['time']

    pending_jobs = [job for job in jobs if job.state == JobState.PENDING]
    running_jobs = [job for job in jobs if job.state == JobState.RUNNING]
    reconfiguring_jobs = [job for job in jobs if job.state == JobState.PENDING_RECONFIGURATION or
                          job.state == JobState.IN_RECONFIGURATION]
    completed_jobs = [job for job in jobs if job.state == JobState.COMPLETED]
    killed_jobs = [job for job in jobs if job.state == JobState.KILLED]

    free_nodes = [node for node in nodes if node.state == NodeState.FREE]
    allocated_nodes = [node for node in nodes if node.state == NodeState.ALLOCATED]
    reserved_nodes = [node for node in nodes if node.state == NodeState.RESERVED]

    for job in jobs:
        if not free_nodes:
            break
        if (job.type == JobType.MOLDABLE or job.type == JobType.MALLEABLE) and job.state == JobState.PENDING:
            num_nodes_to_assign = min(len(free_nodes), job.num_nodes_max)
            if num_nodes_to_assign >= job.num_nodes_min:
                job.assign(free_nodes[:num_nodes_to_assign])
                del free_nodes[:num_nodes_to_assign]
        elif job.type == JobType.MALLEABLE and job.state == JobState.RUNNING:
            num_nodes_to_expand = min(len(free_nodes), job.num_nodes_max - len(job.assigned_nodes))
            if num_nodes_to_expand > 0:
                job.assign(free_nodes[:num_nodes_to_expand])
                del free_nodes[:num_nodes_to_expand]
        elif job.type == JobType.RIGID and job.state == JobState.PENDING:
            if job.num_nodes <= len(free_nodes):
                job.assign(free_nodes[:job.num_nodes])
                del free_nodes[:job.num_nodes]


if __name__ == '__main__':
    url = 'ipc:///tmp/elastisim.ipc'
    pass_algorithm(schedule, url)
