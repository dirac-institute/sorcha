from sorcha.modules.PPModuleRNG import PerModuleRNG


def test_PerModuleRNG():
    rngs = PerModuleRNG(2021)

    rng1 = rngs.getModuleRNG("module1")
    rng2 = rngs.getModuleRNG("module2")
    rng3 = rngs.getModuleRNG("module1")

    # Check that using the same module name gives the same random
    # number generator and a different name gives a different generator.
    assert rng1 is rng3
    assert rng1 is not rng2
    assert rng3 is not rng2
