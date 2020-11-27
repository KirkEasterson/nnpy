from __future__ import print_function
import filecmp, nnpy, sys, unittest

class Tests(unittest.TestCase):
    def test_basic(self):

        pub = nnpy.Socket(nnpy.AF_SP, nnpy.PUB)
        pub.setsockopt(nnpy.SOL_SOCKET, nnpy.IPV4ONLY, 0)
        pub.bind('inproc://foo')
        self.assertEqual(pub.getsockopt(nnpy.SOL_SOCKET, nnpy.DOMAIN), 1)

        sub = nnpy.Socket(nnpy.AF_SP, nnpy.SUB)
        sub_conn = sub.connect('inproc://foo')
        sub.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, '')

        pub.send('FLUB')
        poller = nnpy.PollSet((sub, nnpy.POLLIN))
        self.assertEqual(len(poller.poll()), 1)
        self.assertEqual(poller.poll()[0], 1)
        self.assertEqual(sub.recv().decode(), 'FLUB')
        self.assertEqual(pub.get_statistic(nnpy.STAT_MESSAGES_SENT), 1)
        pub.close()
        sub.shutdown(sub_conn)

    def test_basic_nn_error(self):
        address = 'inproc://timeout-always'

        req = nnpy.Socket(nnpy.AF_SP, nnpy.REQ)
        req.connect(address)

        req.setsockopt(nnpy.SOL_SOCKET, nnpy.RCVTIMEO, 500)

        with self.assertRaises(nnpy.errors.NNError):
            req.recv()

    def test_ptf_code_generator(self):
        
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

def suite():
    return unittest.makeSuite(Tests)

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
