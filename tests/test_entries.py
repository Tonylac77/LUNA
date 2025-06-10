import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from luna.mol.entry import *
from luna.util.exceptions import InvalidEntry, IllegalArgumentError, MoleculeObjectError, MoleculeObjectTypeError, MoleculeNotFoundError


class TestEntry:

    def test_init(self):
        # Missing obligatory parameter.
        import pytest
        with pytest.raises(TypeError):
            Entry("3QL8")

        # Invalid chain id format.
        with pytest.raises(InvalidEntry):
            Entry("3QL8", "AA")

        # Invalid chain id format.
        with pytest.raises(InvalidEntry):
            Entry("3QL8", "+1")

        # Missing obligatory parameter when a compound information is provided.
        with pytest.raises(IllegalArgumentError):
            Entry("3QL8", "A", "NAG")
        with pytest.raises(IllegalArgumentError):
            Entry("3QL8", "A", comp_name="NAG")
        with pytest.raises(IllegalArgumentError):
            Entry("3QL8", "A", comp_num=100)

        # Valid PDB and chain ID formats.
        assert Entry("3QL8", "A").to_string() == "3QL8:A"
        assert Entry("3QL8", "1").to_string() == "3QL8:1"
        assert Entry("3QL8", "A", None, None).to_string() == "3QL8:A"

        # Valid filenames.
        long_filename = "Q411SM6ZMPI6CBUKZSX10IA9M2923PUIHY88URUWC0R1ZOLQLJKXK9VATXRI3CM9W7RU409M19CG6S55TQ5L8L03HIKKL2HSEBTJ2VT7Y4G2JTUB558JOG2F3H9O524MMSYM0M3A347Q2JN77XG4MLAR3XI3EULR6WMVZ6U6NMASHPSUBE28ETOB0S1M0PTDX4KW45KLYC0JL5E77HKLAQK97NNOVB15B4SGVEVSZ90HZ3IMWZLF361AM0M0NSS"
        assert Entry(long_filename, "B").to_string() == f"{long_filename}:B"
        assert Entry('file1.my_test=1a', "B").to_string() == "file1.my_test=1a:B"

        # Long filename.
        with pytest.raises(InvalidEntry):
            Entry("4Q411SM6ZMPI6CBUKZSX10IA9M2923PUIHY88URUWC0R1ZOLQLJKXK9VATXRI3CM9W7RU409M19CG6S55TQ5L8L03HIKKL2HSEBTJ2VT7Y4G2JTUB558JOG2F3H9O524MMSYM0M3A347Q2JN77XG4MLAR3XI3EULR6WMVZ6U6NMASHPSUBE28ETOB0S1M0PTDX4KW45KLYC0JL5E77HKLAQK97NNOVB15B4SGVEVSZ90HZ3IMWZLF361AM0M0NSS", "B")

        # Valid compound entries.
        assert Entry("3QL8", "A", comp_name="X02", comp_num=100).to_string() == "3QL8:A:X02:100"
        assert Entry("3QL8", "A", "X02", 100).to_string() == "3QL8:A:X02:100"
        assert Entry("3QL8", "A", "X02", "100").to_string() == "3QL8:A:X02:100"
        assert Entry("3QL8", "A", 150, "100").to_string() == "3QL8:A:150:100"
        assert Entry("3QL8", "A", "X02", -100).to_string() == "3QL8:A:X02:-100"
        assert Entry("3QL8", "A", "X02", "+100").to_string() == "3QL8:A:X02:100"
        assert Entry("3NS9", "A", "NS9", "0").to_string() == "3NS9:A:NS9:0"

        # Valid compound entries with different compound name forms.
        assert Entry("3QL8", "A", "X", 533).to_string() == "3QL8:A:X:533"
        assert Entry("3QL8", "A", "XA", 533).to_string() == "3QL8:A:XA:533"
        assert Entry("3QL8", "A", "XAA", 533).to_string() == "3QL8:A:XAA:533"
        assert Entry("3QL8", "A", "Cl-", 533).to_string() == "3QL8:A:Cl-:533"
        assert Entry("3QL8", "A", "Na+", 533).to_string() == "3QL8:A:Na+:533"
        assert Entry("3QL8", "A", "NA+", 533).to_string() == "3QL8:A:NA+:533"
        assert Entry("3QL8", "A", "NA-", 533).to_string() == "3QL8:A:NA-:533"
        assert Entry("3QL8", "A", "N++", 533).to_string() == "3QL8:A:N++:533"
        assert Entry("3QL8", "A", "O--", 533).to_string() == "3QL8:A:O--:533"

        # Valid compound entries with Icode
        assert Entry("3QL8", "A", "X01", "100", "A").to_string() == "3QL8:A:X01:100A"

        # Invalid compound entries.
        with pytest.raises(InvalidEntry):
            Entry("3QL8", "A", "X043", 10)
        with pytest.raises(IllegalArgumentError):
            Entry("3QL8", "A", "X01", "XAA")
        with pytest.raises(IllegalArgumentError):
            Entry("3QL8", "A", "X01", "X")
        with pytest.raises(IllegalArgumentError):
            Entry("3QL8", "A", None, "X")
        with pytest.raises(IllegalArgumentError):
            Entry("3QL8", "A", "X01", None)

        # Invalid compound entries with Icode
        with pytest.raises(IllegalArgumentError):
            Entry("3QL8", "A", "X01", 100, "1")
        with pytest.raises(IllegalArgumentError):
            Entry("3QL8", "A", "X01", 100, 1)

    def test_property_update(self):
        import pytest
        entry = Entry("3QL8", "A")

        with pytest.raises(AttributeError):
            entry.pdb_id = "3QQK"

        with pytest.raises(AttributeError):
            entry.chain_id = "C"

        with pytest.raises(AttributeError):
            entry.comp_name = "X05"

        with pytest.raises(AttributeError):
            entry.comp_num = 100

        with pytest.raises(AttributeError):
            entry.comp_icode = "B"

        entry.is_hetatm = False
        assert entry.is_hetatm == False

        entry.sep = "_"
        assert entry.to_string() == "3QL8_A"

    def test_from_string(self):
        # Missing obligatory parameter.
        import pytest
        with pytest.raises(IllegalArgumentError):
            Entry.from_string("3QL8")

        # Invalid chain id format.
        with pytest.raises(InvalidEntry):
            Entry("3QL8", "AA")

        # Invalid chain id format.
        with pytest.raises(InvalidEntry):
            Entry.from_string("3QL8:+1")

        # Missing obligatory parameter when a compound information is provided.
        with pytest.raises(IllegalArgumentError):
            Entry.from_string("3QL8:A:NAG")
        with pytest.raises(IllegalArgumentError):
            Entry.from_string("3QL8:A:100")

        # Valid PDB and chain ID formats.
        assert Entry.from_string("3QL8:A").to_string() == "3QL8:A"
        assert Entry.from_string("3QL8:1").to_string() == "3QL8:1"
        assert Entry.from_string("3QL8-A", sep="-").to_string() == "3QL8-A"
        assert Entry.from_string("3QL8_A", sep="_").to_string() == "3QL8_A"

        # Valid filenames.
        long_filename = "Q411SM6ZMPI6CBUKZSX10IA9M2923PUIHY88URUWC0R1ZOLQLJKXK9VATXRI3CM9W7RU409M19CG6S55TQ5L8L03HIKKL2HSEBTJ2VT7Y4G2JTUB558JOG2F3H9O524MMSYM0M3A347Q2JN77XG4MLAR3XI3EULR6WMVZ6U6NMASHPSUBE28ETOB0S1M0PTDX4KW45KLYC0JL5E77HKLAQK97NNOVB15B4SGVEVSZ90HZ3IMWZLF361AM0M0NSS"
        assert Entry.from_string(f"{long_filename}:B").to_string() == f"{long_filename}:B"
        assert Entry.from_string('file1.my_test=1a:B').to_string() == "file1.my_test=1a:B"

        # Long filename.
        with pytest.raises(InvalidEntry):
            Entry.from_string("4Q411SM6ZMPI6CBUKZSX10IA9M2923PUIHY88URUWC0R1ZOLQLJKXK9VATXRI3CM9W7RU409M19CG6S55TQ5L8L03HIKKL2HSEBTJ2VT7Y4G2JTUB558JOG2F3H9O524MMSYM0M3A347Q2JN77XG4MLAR3XI3EULR6WMVZ6U6NMASHPSUBE28ETOB0S1M0PTDX4KW45KLYC0JL5E77HKLAQK97NNOVB15B4SGVEVSZ90HZ3IMWZLF361AM0M0NSS:B")

        # Valid compound entries.
        assert Entry.from_string("3QL8:A:X02:100").to_string() == "3QL8:A:X02:100"
        assert Entry.from_string("3QL8:A:150:100").to_string() == "3QL8:A:150:100"
        assert Entry.from_string("3QL8:A:X02:-100").to_string() == "3QL8:A:X02:-100"
        assert Entry.from_string("3QL8:A:X02:+100").to_string() == "3QL8:A:X02:100"

        # Valid compound entries with different compound name forms.
        assert Entry.from_string("3QL8:A:X:533").to_string() == "3QL8:A:X:533"
        assert Entry.from_string("3QL8:A:XA:533").to_string() == "3QL8:A:XA:533"
        assert Entry.from_string("3QL8:A:XAA:533").to_string() == "3QL8:A:XAA:533"
        assert Entry.from_string("3QL8:A:Cl-:533").to_string() == "3QL8:A:Cl-:533"
        assert Entry.from_string("3QL8:A:Na+:533").to_string() == "3QL8:A:Na+:533"
        assert Entry.from_string("3QL8:A:NA+:533").to_string() == "3QL8:A:NA+:533"
        assert Entry.from_string("3QL8:A:NA-:533").to_string() == "3QL8:A:NA-:533"
        assert Entry.from_string("3QL8:A:N++:533").to_string() == "3QL8:A:N++:533"
        assert Entry.from_string("3QL8:A:O--:533").to_string() == "3QL8:A:O--:533"
        assert Entry.from_string("3QL8:A:X02:9999").to_string() == "3QL8:A:X02:9999"

        # Valid compound entries with Icode
        assert Entry.from_string("3QL8:A:X01:100A").to_string() == "3QL8:A:X01:100A"

        # Invalid compound entries.
        with pytest.raises(InvalidEntry):
            Entry.from_string("3QL8:A:X043:10")
        with pytest.raises(InvalidEntry):
            Entry.from_string("3QL8:A:X02:99999")
        with pytest.raises(IllegalArgumentError):
            Entry.from_string("3QL8:A:X04:10:A")
        with pytest.raises(IllegalArgumentError):
            Entry.from_string("3QL8:A:X04:10:A:10")
        with pytest.raises(IllegalArgumentError):
            Entry.from_string("3QL8:A:X01:XAA")
        with pytest.raises(IllegalArgumentError):
            Entry.from_string("3QL8:A:X01:X")
        with pytest.raises(IllegalArgumentError):
            Entry.from_string("3QL8:A:None:X")
        with pytest.raises(IllegalArgumentError):
            Entry.from_string("3QL8:A:X01")

    def test_get_biopython_key(self):
        entry = Entry("3QL8", "A")
        assert entry.get_biopython_key() == "A"

        entry = Entry("3QL8", "A", "X02", 104)
        assert entry.get_biopython_key() == ("H_X02", 104, " ")

        entry = Entry("3QL8", "A", "X02", 104, "A")
        assert entry.get_biopython_key() == ("H_X02", 104, "A")

        entry = Entry("3QL8", "A", "X02", 104, " ")
        assert entry.get_biopython_key() == ("H_X02", 104, " ")

        entry = Entry("3QL8", "A", "X02", 104, None)
        assert entry.get_biopython_key() == ("H_X02", 104, " ")

        entry = Entry("3QL8", "A", "X02", 104, is_hetatm=False)
        assert entry.get_biopython_key() == (" ", 104, " ")

        entry = Entry("3QL8", "A", "HOH", 104, is_hetatm=False)
        assert entry.get_biopython_key() == ("W", 104, " ")

        entry = Entry("3QL8", "A", "HOH", 104, is_hetatm=True)
        assert entry.get_biopython_key() == ("W", 104, " ")

        entry = Entry("3QL8", "A", "WAT", 104, is_hetatm=False)
        assert entry.get_biopython_key() == ("W", 104, " ")


