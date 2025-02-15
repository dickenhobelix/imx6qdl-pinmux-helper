import pytest
from pinmux_helper_imx6 import pinmux_generator


def test_generate_hys():
    assert (1 << 16) == (
        (1 << 16)
        & int(
            pinmux_generator.generate_pinmux_option(
                "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
            ),
            0,
        )
    )
    assert (1 << 16) != (
        (1 << 16)
        & int(
            pinmux_generator.generate_pinmux_option(
                "HYS_CMOS PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
            ),
            0,
        )
    )
    with pytest.raises(Exception) as ex:
        str(
            pinmux_generator.generate_pinmux_option(
                "PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
            )
        )
    assert "no HYS value passed, use -h for valid options" in str(ex.value)


def test_generate_pus():
    assert 0 == (
        0x3
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
                ),
                0,
            )
            >> 14
        )
    )
    assert 1 == (
        0x3
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_47K_UP PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
                ),
                0,
            )
            >> 14
        )
    )
    assert 2 == (
        0x3
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_UP PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
                ),
                0,
            )
            >> 14
        )
    )
    assert 3 == (
        0x3
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_22K_UP PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
                ),
                0,
            )
            >> 14
        )
    )
    with pytest.raises(Exception) as ex:
        str(
            pinmux_generator.generate_pinmux_option(
                "HYS_SCHMITT PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
            )
        )
    assert "no PUS value passed, use -h for valid options" in str(ex.value)


def test_generate_pue():
    assert (1 << 13) == (
        (1 << 13)
        & int(
            pinmux_generator.generate_pinmux_option(
                "HYS_SCHMITT PUS_100K_DOWN PUE_PULL PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
            ),
            0,
        )
    )
    assert (1 << 13) != (
        (1 << 13)
        & int(
            pinmux_generator.generate_pinmux_option(
                "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
            ),
            0,
        )
    )
    with pytest.raises(Exception) as ex:
        str(
            pinmux_generator.generate_pinmux_option(
                "HYS_SCHMITT PUS_100K_DOWN PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
            )
        )
    assert "no PUE value passed, use -h for valid options" in str(ex.value)


def test_generate_pke():
    assert (1 << 12) == (
        (1 << 12)
        & int(
            pinmux_generator.generate_pinmux_option(
                "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
            ),
            0,
        )
    )
    assert (1 << 12) != (
        (1 << 12)
        & int(
            pinmux_generator.generate_pinmux_option(
                "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_DISABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
            ),
            0,
        )
    )
    with pytest.raises(Exception) as ex:
        str(
            pinmux_generator.generate_pinmux_option(
                "HYS_SCHMITT PUS_100K_DOWN PUE_PULL ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
            )
        )
    assert "no PKE value passed, use -h for valid options" in str(ex.value)


def test_generate_ode():
    assert (1 << 11) == (
        (1 << 11)
        & int(
            pinmux_generator.generate_pinmux_option(
                "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
            ),
            0,
        )
    )
    assert (1 << 11) != (
        (1 << 11)
        & int(
            pinmux_generator.generate_pinmux_option(
                "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_DISABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
            ),
            0,
        )
    )
    with pytest.raises(Exception) as ex:
        str(
            pinmux_generator.generate_pinmux_option(
                "HYS_SCHMITT PUS_100K_DOWN PUE_PULL PKE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
            )
        )
    assert "no ODE value passed, use -h for valid options" in str(ex.value)


def test_generate_speed():
    assert 1 == (
        0x3
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
                ),
                0,
            )
            >> 6
        )
    )
    assert 2 == (
        0x3
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE MED_SPEED DSE_DISABLE SRE_SLOW"
                ),
                0,
            )
            >> 6
        )
    )
    assert 3 == (
        0x3
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE HIGH_SPEED DSE_DISABLE SRE_SLOW"
                ),
                0,
            )
            >> 6
        )
    )
    with pytest.raises(Exception) as ex:
        str(
            pinmux_generator.generate_pinmux_option(
                "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE DSE_DISABLE SRE_SLOW"
            )
        )
    assert "no SPEED value passed, use -h for valid options" in str(ex.value)


def test_generate_dse():
    assert 0 == (
        0x7
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
                ),
                0,
            )
            >> 3
        )
    )
    assert 0 == (
        0x7
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_HIZ SRE_SLOW"
                ),
                0,
            )
            >> 3
        )
    )
    assert 1 == (
        0x7
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_240OHM SRE_SLOW"
                ),
                0,
            )
            >> 3
        )
    )
    assert 2 == (
        0x7
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_120OHM SRE_SLOW"
                ),
                0,
            )
            >> 3
        )
    )
    assert 3 == (
        0x7
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_80OHM SRE_SLOW"
                ),
                0,
            )
            >> 3
        )
    )
    assert 4 == (
        0x7
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_60OHM SRE_SLOW"
                ),
                0,
            )
            >> 3
        )
    )
    assert 5 == (
        0x7
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_48OHM SRE_SLOW"
                ),
                0,
            )
            >> 3
        )
    )
    assert 6 == (
        0x7
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_40OHM SRE_SLOW"
                ),
                0,
            )
            >> 3
        )
    )
    assert 7 == (
        0x7
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_34OHM SRE_SLOW"
                ),
                0,
            )
            >> 3
        )
    )
    with pytest.raises(Exception) as ex:
        str(
            pinmux_generator.generate_pinmux_option(
                "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED SRE_SLOW"
            )
        )
    assert "no DSE value passed, use -h for valid options" in str(ex.value)


def test_generate_speed():
    assert 1 == (
        0x1
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_FAST"
                ),
                0,
            )
        )
    )
    assert 0 == (
        0x1
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
                ),
                0,
            )
        )
    )
    assert 0 == (
        0x1
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE"
                ),
                0,
            )
        )
    )


def test_generate_SION():
    assert 1 == (
        0x1
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_FAST SION"
                ),
                0,
            )
            >> 30
        )
    )
    assert 0 == (
        0x1
        & (
            int(
                pinmux_generator.generate_pinmux_option(
                    "HYS_SCHMITT PUS_100K_DOWN PUE_KEEP PKE_ENABLE ODE_ENABLE LOW_SPEED DSE_DISABLE SRE_SLOW"
                ),
                0 >> 30,
            )
        )
    )
