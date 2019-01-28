#!/usr/bin/env python3

"""
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * - Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer.
 *
 * - Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * - Neither the name of prim nor the names of its contributors may be used to
 * endorse or promote products derived from this software without specific prior
 * written permission.
 *
 * See the NOTICE file distributed with this work for additional information
 * regarding copyright ownership.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
"""

import argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import ssplot
import subprocess
import taskrun

def fattree_size(radix, levels, data, idx):
  size = radix
  for level in range(levels - 1):
    if level % 2 == 0:
      size *= (radix // 2)
    else:
      size *= (radix - (radix // 2))
    data[idx] = size

def hyperx_size(radix, dimensions, data, idx):
  cmd = ('~/dev/hyperxsearch/scripts/hyperx_flat_search.py '
         '~/dev/hyperxsearch/bin/hyperxsearch '
         '{0} {0} {1} 0.5'.format(radix, dimensions))
  proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
  data[idx] = int(proc.stdout.decode('utf-8').split('\n')[1].split()[5])

def dragonfly_size(radix, data, idx):
  cmd = ('~/dev/hyperxsearch/scripts/hyperx_hierarchical_search.py '
         '~/dev/hyperxsearch/bin/hyperxsearch '
         '{0} {0} 1 1 0.5'.format(radix))
  proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
  data[idx] = int(proc.stdout.decode('utf-8').split('\n')[2].split()[5])

def dragonflyplus_size(radix, minus, data, idx):
  links = (radix // 2) * (radix - (radix // 2))
  if not minus:
    data[idx] = links * (links + 1)
  else:
    data[idx] = links * ((radix // 2) + 1)

def main(args):
  # build the task manager
  cpus = os.cpu_count()
  mem = taskrun.MemoryResource.current_available_memory_gib();
  rm = taskrun.ResourceManager(taskrun.CounterResource('cpus', 1, cpus))
  vob = taskrun.VerboseObserver(description=False, summary=True)
  tm = taskrun.TaskManager(resource_manager=rm,
                           observers=[vob],
                           failure_mode=taskrun.FailureMode.AGGRESSIVE_FAIL)

  # create generator tasks
  num_radices = args.stop - args.start + 1
  radices = range(args.start, args.stop + 1)
  topo_sizes = []
  topo_names = []
  skipped_topos = []
  topo_index = 0

  # 2L Fat Tree
  name = '2L Fat Tree (3)'
  if not args.skip or name not in args.skip:
    topo_names.append(name)
    topo_sizes.append([0] * num_radices)
    for idx, radix in enumerate(radices):
      task = taskrun.FunctionTask(tm, 'fattree_2l-{}'.format(radix),
                                  fattree_size, radix, 2,
                                  topo_sizes[topo_index], idx)
    topo_index += 1
  else:
    skipped_topos.append(name)

  # 3L Fat Tree
  name = '3L Fat Tree (5)'
  if not args.skip or name not in args.skip:
    topo_names.append(name)
    topo_sizes.append([0] * num_radices)
    for idx, radix in enumerate(radices):
      task = taskrun.FunctionTask(tm, 'fattree_3l-{}'.format(radix),
                                  fattree_size, radix, 3,
                                  topo_sizes[topo_index], idx)
    topo_index += 1
  else:
    skipped_topos.append(name)

  # 1D HyperX
  name = '1D HyperX (2)'
  if not args.skip or name not in args.skip:
    topo_names.append(name)
    topo_sizes.append([0] * num_radices)
    for idx, radix in enumerate(radices):
      task = taskrun.FunctionTask(tm, 'hyperx_1d-{}'.format(radix),
                                  hyperx_size, radix, 1,
                                  topo_sizes[topo_index], idx)
    topo_index += 1
  else:
    skipped_topos.append(name)

  # 2D HyperX
  name = '2D HyperX (3)'
  if not args.skip or name not in args.skip:
    topo_names.append(name)
    topo_sizes.append([0] * num_radices)
    for idx, radix in enumerate(radices):
      task = taskrun.FunctionTask(tm, 'hyperx_2d-{}'.format(radix),
                                  hyperx_size, radix, 2,
                                  topo_sizes[topo_index], idx)
    topo_index += 1
  else:
    skipped_topos.append(name)

  # 3D HyperX
  name = '3D HyperX (4)'
  if not args.skip or name not in args.skip:
    topo_names.append(name)
    topo_sizes.append([0] * num_radices)
    for idx, radix in enumerate(radices):
      task = taskrun.FunctionTask(tm, 'hyperx_3d-{}'.format(radix),
                                  hyperx_size, radix, 3,
                                  topo_sizes[topo_index], idx)
    topo_index += 1
  else:
    skipped_topos.append(name)

  # 4D HyperX
  name = '4D HyperX (5)'
  if not args.skip or name not in args.skip:
    topo_names.append(name)
    topo_sizes.append([0] * num_radices)
    for idx, radix in enumerate(radices):
      task = taskrun.FunctionTask(tm, 'hyperx_4d-{}'.format(radix),
                                  hyperx_size, radix, 4,
                                  topo_sizes[topo_index], idx)
    topo_index += 1
  else:
    skipped_topos.append(name)

  # Dragonfly
  name = 'Dragonfly (4)'
  if not args.skip or name not in args.skip:
    topo_names.append(name)
    topo_sizes.append([0] * num_radices)
    for idx, radix in enumerate(radices):
      task = taskrun.FunctionTask(tm, 'dragonfly-{}'.format(radix),
                                  dragonfly_size, radix,
                                  topo_sizes[topo_index], idx)
    topo_index += 1
  else:
    skipped_topos.append(name)

  # Dragonfly+
  name = 'Dragonfly+ (4)'
  if not args.skip or name not in args.skip:
    topo_names.append(name)
    topo_sizes.append([0] * num_radices)
    for idx, radix in enumerate(radices):
      task = taskrun.FunctionTask(tm, 'dragonflyplus-{}'.format(radix),
                                  dragonflyplus_size, radix, False,
                                  topo_sizes[topo_index], idx)
    topo_index += 1
  else:
    skipped_topos.append(name)

  # FatDragon a.k.a. Dragonfly+-
  name = 'Fat Dragon (4)'
  if not args.skip or name not in args.skip:
    topo_names.append(name)
    topo_sizes.append([0] * num_radices)
    for idx, radix in enumerate(radices):
      task = taskrun.FunctionTask(tm, 'fatdragon-{}'.format(radix),
                                  dragonflyplus_size, radix, True,
                                  topo_sizes[topo_index], idx)
    topo_index += 1
  else:
    skipped_topos.append(name)

  # check skip list
  if args.skip:
    for topo in args.skip:
      assert topo in topo_names or topo in skipped_topos, \
        '"{}" not a valid topology'.format(topo)

  # print topologies option
  if args.list:
    for topo in topo_names:
      print(topo)
    return

  # run all tasks
  tm.run_tasks()

  # CSV output file
  if args.csv:
    with open(args.csv, 'w') as fd:
      cols = 1 + len(topo_names)
      fd.write('Radix')
      for topo in topo_names:
        fd.write(',{}'.format(topo))
      fd.write('\n')
      for radix_idx, radix in enumerate(radices):
        fd.write('{}'.format(radix))
        for topo_idx, topo in enumerate(topo_names):
          fd.write(',{}'.format(topo_sizes[topo_idx][radix_idx]))
        fd.write('\n')

  # plot the results
  mlp = ssplot.MultilinePlot(plt, list(radices), topo_sizes)
  mlp.set_data_labels(topo_names)
  mlp.set_xlabel('Router Radix')
  #mlp.set_ymin(2**8)
  #mlp.set_ymax(2**24 * 1.9)
  mlp.set_ylabel('Maximum Topology Size')
  mlp.set_yscale('log2')
  mlp.set_yticklabels_verbose(True)
  mlp.set_plot_style('inferno-markers')
  mlp.set_figure_size('10x6')
  mlp.set_legend_columns(2)
  mlp.plot(args.plot)

  # crop the figure (i.e., remove margin whitespace)
  subprocess.run('convert {0} -trim {0}'.format(args.plot), shell=True)

if __name__ == '__main__':
  ap = argparse.ArgumentParser()
  ap.add_argument('start', type=int,
                  help='starting radix')
  ap.add_argument('stop', type=int,
                  help='stopping radix')
  ap.add_argument('plot', type=str,
                  help='output plot filename')
  ap.add_argument('--list', action='store_true',
                  help='print list of topologies and exit')
  ap.add_argument('--skip', nargs='*', type=str,
                  help='topologies to skip')
  ap.add_argument('--csv', default=None,
                  help='CSV file for output data')
  args = ap.parse_args()
  assert args.start >= 2
  assert args.start <= args.stop
  main(args)
