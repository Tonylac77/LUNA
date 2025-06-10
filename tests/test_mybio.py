import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from luna.MyBio.PDB.Model import Model
from luna.MyBio.PDB.Chain import Chain
from luna.MyBio.extractor import Extractor


class TestExtractor:

    def test_init(self):
        # Wrong type.
        import pytest
        with pytest.raises(TypeError):
            Extractor("3QL8")
        with pytest.raises(TypeError):
            Extractor(1)
        with pytest.raises(TypeError):
            Extractor(int)
        with pytest.raises(TypeError):
            Extractor(self)
        with pytest.raises(TypeError):
            Extractor(Chain)
        with pytest.raises(TypeError):
            Extractor(None)

        # Wrong initialization.
        with pytest.raises(TypeError):
            Extractor(Chain())
        # Wrong initialization.
        with pytest.raises(TypeError):
            Extractor(Model())

        # Extractor correctly initialized.
        model = Model(0)
        extractor = Extractor(model)
        assert extractor.entity.id == model.id
        assert extractor.entity.id != "A"
        assert extractor.entity.id != 1

        extractor.extract_chains(["A"], "test.pdb")

        # Extractor correctly initialized.
        chain = Chain("A")
        extractor = Extractor(chain)
        assert extractor.entity.id == chain.id
        assert extractor.entity.id != "B"
        assert extractor.entity.id != 1


