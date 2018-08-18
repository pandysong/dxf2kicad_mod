import unittest
import kicad_mod_format as kf


class TestKicadModeFormat(unittest.TestCase):

    def test_Module(self):
        expects = (
            "(module dxfgeneratedcopper\n",
            "    (layer F.cu)\n",
            "    (tedit 0)\n",
            "    (fp_text reference G***\n",
            "        (at 0 -4)\n",
            "        (layer F.SilkS)\n",
            "        hide\n",
            "        (effects\n",
            "            (font\n",
            "                (thickness 0.2))))\n",
            "    (fp_text value value\n",
            "        (at 0 4)\n",
            "        (layer F.SilkS)\n",
            "        hide\n",
            "        (effects\n",
            "            (font\n",
            "                (thickness 0.2))))\n",
            "    (layer F.cu)\n",
            "    (tedit 0))")
        self.assertEqual(''.join(expects),
                         str(kf.Module('dxfgeneratedcopper',
                                       children=(kf.layer('F.cu'),
                                                 kf.tedit(0))
                                       )))


if __name__ == '__main__':
    unittest.main()
