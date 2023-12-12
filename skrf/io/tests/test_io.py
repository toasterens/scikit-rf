import unittest
import os
import numpy as npy

import skrf as rf
from skrf.io import Touchstone
from skrf.io import network_2_dataframe

class IOTestCase(unittest.TestCase):
    """
    """
    def setUp(self):
        """
        """
        self.test_dir = os.path.dirname(os.path.abspath(__file__))+'/'
        self.pickle_file = os.path.join(self.test_dir, 'pickled.p')
        self.hfss_oneport_file = os.path.join(self.test_dir, 'hfss_oneport.s1p')
        self.hfss_twoport_file = os.path.join(self.test_dir, 'hfss_twoport.s2p')
        self.ntwk1 = rf.Network(os.path.join(self.test_dir, 'ntwk1.s2p'))
        self.ntwk2 = rf.Network(os.path.join(self.test_dir, 'ntwk2.s2p'))
        self.ntwk3 = rf.Network(os.path.join(self.test_dir, 'ntwk3.s2p'))
        self.short = rf.Network(os.path.join(self.test_dir, 'short.s1p'))
        self.match = rf.Network(os.path.join(self.test_dir, 'match.s1p'))
        self.open = rf.Network(os.path.join(self.test_dir, 'open.s1p'))
        self.ntwk_comments_file = os.path.join(self.test_dir, 'comments.s3p')
        self.test_files = [os.path.join(self.test_dir, test_file) for test_file in ['ntwk1.s2p', 'ntwk2.s2p']]
        self.embeding_network= rf.Network(os.path.join(self.test_dir, 'embedingNetwork.s2p'))
        self.freq = rf.F(75, 110, 101, unit='GHz')

    def read_write(self,obj):
        """
        function to test write/read equivalence for an obj which has
        __eq__ defined
        """
        rf.write(self.pickle_file,obj)
        self.assertEqual(rf.read(self.pickle_file), obj)
       # os.remove(self.pickle_file)



    def test_read_all(self):
        rf.read_all(self.test_dir)

    def test_read_all_files(self):
        rf.read_all(files=self.test_files)

    def test_save_sesh(self):
        a=self.ntwk1
        b=self.ntwk2
        c=self.ntwk3
        rf.save_sesh(locals(),self.pickle_file )
        #os.remove(self.pickle_file)

    def test_write_all_dict(self):
        d = dict(a=self.ntwk1, b=self.ntwk2,   c=self.ntwk3)
        rf.write_all(d, dir =self.test_dir )
        os.remove(os.path.join(self.test_dir, 'a.ntwk'))
        os.remove(os.path.join(self.test_dir, 'b.ntwk'))
        os.remove(os.path.join(self.test_dir, 'c.ntwk'))

    def test_readwrite_network(self):
        self.read_write(self.ntwk1)

    def test_readwrite_list_of_network(self):
        self.read_write([self.ntwk1, self.ntwk2])

    def test_readwrite_networkSet(self):
        """
        test_readwrite_networkSet
        TODO: need __eq__ method for NetworkSet
        This doesnt test equality between  read/write, because there is no
        __eq__ test for NetworkSet. it only tests for other errors
        """
        rf.write(self.pickle_file,rf.NS([self.ntwk1, self.ntwk2]))
        rf.read(self.pickle_file)
        #self.assertEqual(rf.read(self.pickle_file), rf.NS([self.ntwk1, self.ntwk2])
        #os.remove(self.pickle_file)

    def test_readwrite_frequency(self):
        freq = rf.Frequency(1,10,10,'ghz')
        self.read_write(freq)

    def test_readwrite_calibration(self):
        ideals, measured = [], []
        std_list = [self.short, self.match,self.open]

        for ntwk in std_list:
            ideals.append(ntwk)
            measured.append(self.embeding_network ** ntwk)

        cal = rf.Calibration(\
                ideals = ideals,\
                measured = measured,\
                type = 'one port',\
                is_reciprocal = True,\
                )

        original = cal
        rf.write(self.pickle_file, original)
        unpickled = rf.read(self.pickle_file)
        # TODO: this test should be more extensive
        self.assertEqual(original.ideals, unpickled.ideals)
        self.assertEqual(original.measured, unpickled.measured)

        os.remove(self.pickle_file)

    def test_readwrite_media(self):
        a_media = rf.media.DefinedGammaZ0(
            frequency = self.freq,
            gamma = 1j*npy.ones(101) ,
            z0 =  50*npy.ones(101),
            )
        self.read_write(a_media)
    @unittest.skip
    def test_readwrite_media_func_propgamma(self):
        a_media = rf.media.Media(
            frequency = self.freq,
            propagation_constant = lambda :1j ,
            characteristic_impedance =  lambda :50,
            )
        self.read_write(a_media)
    @unittest.skip
    def test_readwrite_RectangularWaveguide(self):
        a_media = rf.media.RectangularWaveguide(
            frequency = self.freq,
            a=100*rf.mil,
            z0=50,
            )
        self.read_write(a_media)
    @unittest.skip
    def test_readwrite_DistributedCircuit(self):
        one = npy.ones(self.freq.npoints)
        a_media = rf.media.DistributedCircuit(
            frequency = self.freq,
            R=1e5*one, G=1*one, I=1e-6*one, C=8e-12*one
            )
        self.read_write(a_media)
    @unittest.skip
    def test_readwrite_Freespace(self):
        a_media = rf.media.Freespace(
            frequency = self.freq,
            )
        self.read_write(a_media)

    def test_snp_json_roundtrip(self):
        """
        Tests if snp object saved to json and reloaded is still the same.
        """
        given = self.ntwk1
        actual = rf.from_json_string(rf.to_json_string(given))
        self.assertEqual(actual, given)
        self.assertEqual(actual.frequency, given.frequency)
        self.assertEqual(actual.name, given.name)
        self.assertEqual(actual.comments, given.comments)
        self.assertEqual(actual.z0.tolist(), given.z0.tolist())
        self.assertEqual(actual.port_names, given.port_names)
        self.assertEqual(actual.variables, given.variables)

    def test_touchstone_get_comment_variables(self):
        """
        Tests if comments are parsed correctly with get_comment_variables() method.
        """

        given = {'p1': ('.03', ''), 'p2': ('0.03', ''), 'p3': ('100', ''), 'p4': ('2.5', 'um')}
        actual = Touchstone(self.ntwk_comments_file).get_comment_variables()
        self.assertEqual(given, actual)

    def test_network_2_dataframe_equal(self):
        df_method = self.ntwk1.to_dataframe()
        df_function = network_2_dataframe(self.ntwk1)

        assert df_method.equals(df_function)

    def test_network_2_dataframe_columns(self):
        s = npy.random.standard_normal((1, 11, 11))
        f = [1]
        netw = rf.Network(s=s, f=f)

        df = netw.to_dataframe()
        assert s.size == df.values.size
        assert "s_db 1_11" in df.columns
        assert "s_db 11_1" in df.columns

    def test_network_2_dataframe_port_sep(self):
        for port_sep in ["", "_", ","]:
            df = self.ntwk1.to_dataframe(port_sep=port_sep)

            assert len(df.columns == self.ntwk1.nports ** 2)
            assert f"s_db 2{port_sep}1" in df.columns

    def test_network_2_dataframe_port_sep_auto(self):
        f = [1]
        for ports in [1, 2, 4, 8, 10, 11, 16]:
            s = npy.random.standard_normal((1, ports, ports))
            netw = rf.Network(s=s, f=f)

            df = netw.to_dataframe()
            
            if ports <= 10:
                assert "s_db 11" in df.columns
            else:
                assert "s_db 1_1" in df.columns