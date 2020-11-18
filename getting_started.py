import sys
import nnpy
import unittest
import filecmp

# Redirect stdout
sys.stdout = open('nnpy_stdout.txt', 'w')
sys.stderr = open('nnpy_stderr.txt', 'w')


pub = nnpy.Socket(nnpy.AF_SP, nnpy.PUB)
pub.bind('inproc://foo')

sub = nnpy.Socket(nnpy.AF_SP, nnpy.SUB)
sub.connect('inproc://foo')
sub.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, '')

pub.send('hello, world')
print(sub.recv())

pub.close()
sub.close()

assert(filecmp.cmp("nnpy_stdout.txt", "ptf_generator_stdout.txt"))
assert(filecmp.cmp("nnpy_stderr.txt", "ptf_generator_stderr.txt"))