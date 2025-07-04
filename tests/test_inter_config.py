from os.path import dirname, abspath
import sys

luna_path = dirname(dirname(abspath(__file__)))
sys.path.append(luna_path)

from luna.interaction.config import (InteractionConfig,
                                     DefaultInteractionConfig)


class TestInteractionConfig:

    def test_init(self):

        # Wrong type.
        import pytest
        with pytest.raises(ValueError):
            InteractionConfig("error")
        with pytest.raises(TypeError):
            InteractionConfig(1)
        with pytest.raises(TypeError):
            InteractionConfig({1, 2, 3})
        with pytest.raises(TypeError):
            InteractionConfig([1, 2, 3])
        with pytest.raises(TypeError):
            DefaultInteractionConfig("error")
        with pytest.raises(TypeError):
            DefaultInteractionConfig(1)
        with pytest.raises(TypeError):
            DefaultInteractionConfig({1, 2, 3})
        with pytest.raises(TypeError):
            DefaultInteractionConfig([1, 2, 3])
        with pytest.raises(TypeError):
            DefaultInteractionConfig({"param1": 2.5, "param2": 5})
        with pytest.raises(TypeError):
            DefaultInteractionConfig(None)

        # Correctly initialized.
        config = InteractionConfig()
        assert config == {}
        config = InteractionConfig(None)
        assert config == {}
        config = InteractionConfig([])
        assert config == {}

        # Correctly initialized.
        config = InteractionConfig([("param1", 2.5), ("param2", 5)])
        assert config["param1"] == 2.5
        assert config["param2"] == 5

        # Correctly initialized.
        config = InteractionConfig({"param1": 2.5, "param2": 5})
        assert config["param1"] == 2.5
        assert config["param2"] == 5

        # Correctly initialized.
        config = InteractionConfig()
        config["param1"] = 2.5
        config["param2"] = 2
        assert config["param1"] == 2.5
        assert config["param2"] == 2
        assert config["param2"] != 5

        # Correctly initialized.
        config = InteractionConfig({"param1": 2.5, "param2": 5})
        assert config.params == ['param1', 'param2']

        # Correctly initialized.
        config = DefaultInteractionConfig()
        assert sorted(config.params) == sorted(['bsite_cutoff',
                                 'cache_cutoff',
                                 'max_an_ey_ang_ortho_multipolar_inter',
                                 'max_an_ey_ang_para_multipolar_inter',
                                 'max_cc_dist_amide_pi_inter',
                                 'max_cc_dist_pi_pi_inter',
                                 'max_da_dist_hb_inter',
                                 'max_da_dist_whb_inter',
                                 'max_dc_dist_whb_inter',
                                 'max_dihed_ang_amide_pi_inter',
                                 'max_dihed_ang_slope_pi_pi_inter',
                                 'max_disp_ang_ion_multipole_inter',
                                 'max_disp_ang_multipolar_inter',
                                 'max_disp_ang_offset_pi_pi_inter',
                                 'max_disp_ang_pi_pi_inter',
                                 'max_disp_ang_whb_inter',
                                 'max_disp_ang_xbond_inter',
                                 'max_disp_ang_ybond_inter',
                                 'max_dist_attract_inter',
                                 'max_dist_cation_pi_inter',
                                 'max_dist_hydrop_inter',
                                 'max_dist_proximal',
                                 'max_dist_repuls_inter',
                                 'max_ha_dist_hb_inter',
                                 'max_ha_dist_whb_inter',
                                 'max_hc_dist_whb_inter',
                                 'max_id_dist_ion_multipole_inter',
                                 'max_ma_dist_metal_coord',
                                 'max_ne_dist_multipolar_inter',
                                 'max_ney_ang_multipolar_inter',
                                 'max_xa_dist_xbond_inter',
                                 'max_xc_dist_xbond_inter',
                                 'max_ya_dist_ybond_inter',
                                 'max_yc_dist_ybond_inter',
                                 'min_an_ey_ang_antipara_multipolar_inter',
                                 'min_an_ey_ang_ortho_multipolar_inter',
                                 'min_bond_separation',
                                 'min_bond_separation_for_clash',
                                 'min_cxa_ang_xbond_inter',
                                 'min_dar_ang_hb_inter',
                                 'min_dar_ang_whb_inter',
                                 'min_dha_ang_hb_inter',
                                 'min_dha_ang_whb_inter',
                                 'min_dhc_ang_whb_inter',
                                 'min_dihed_ang_slope_pi_pi_inter',
                                 'min_disp_ang_offset_pi_pi_inter',
                                 'min_dist_proximal',
                                 'min_har_ang_hb_inter',
                                 'min_har_ang_whb_inter',
                                 'min_idy_ang_ion_multipole_inter',
                                 'min_inter_atom_in_surf',
                                 'min_ney_ang_multipolar_inter',
                                 'min_rya_ang_ybond_inter',
                                 'min_surf_size',
                                 'min_xar_ang_xbond_inter',
                                 'min_yan_ang_ybond_inter',
                                 'vdw_clash_tolerance',
                                 'vdw_tolerance'])

        config["boundary_cutoff"] = 5
        assert config["boundary_cutoff"] == 5

        # Access to nonexistent keys.
        config = DefaultInteractionConfig()
        import pytest
        with pytest.raises(KeyError):
            config["error"]

        # Access to removed keys.
        config = InteractionConfig({"param1": 2.5})
        del config["param1"]
        with pytest.raises(KeyError):
            config["param1"]

        # Access to nonexistent attributes.
        config = InteractionConfig({"param1": 2.5})
        with pytest.raises(AttributeError):
            config.param1


