import angr
import sys
from pwn import *
import claripy

GOOD = "Congratulations !"
BAD  = "Bruh : ("
BASE = 0x400000

def main(argv):
  path_to_binary = "./angry"

  project = angr.Project(path_to_binary, main_opts={"base_addr": BASE})

  flag_chars = [claripy.BVS('flag_%d' % i, 8) for i in range(40)]
  flag = claripy.Concat(*flag_chars+[claripy.BVV(b'\n')])

  initial_state = project.factory.entry_state(
    add_options = { angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY,
                    angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS},
                    stdin=flag
  )
  initial_state.solver.add(flag_chars[0]==ord('L'))
  initial_state.solver.add(flag_chars[1]==ord('3'))
  initial_state.solver.add(flag_chars[2]==ord('A'))
  initial_state.solver.add(flag_chars[3]==ord('K'))
  initial_state.solver.add(flag_chars[4]==ord('{'))

  simulation = project.factory.simgr(initial_state)

  def good_path(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return GOOD.encode() in stdout_output  

  def bad_path(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return BAD.encode() in stdout_output 

  simulation.explore(find=good_path, avoid=bad_path)

  if simulation.found:
    print("Solution: {%s}" %simulation.found[0].posix.dumps(sys.stdin.fileno()))
  else:
    print("no")

if __name__ == '__main__':
  main(sys.argv)
  #L3AK{angr_4_l1f3_d0nt_do_it_m4nU4lly}