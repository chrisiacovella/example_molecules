"""
Unit and regression test for the example_molecules package.
"""

# Import package, test suite, and other packages as needed
import example_molecules
import pytest
import sys
import mbuild as mb

def test_example_molecules_imported():
    """ Sample test, will always pass so long as import statement worked """
    assert "example_molecules" in sys.modules

def test_import():
    """ Test that mBuild recipe import works """
    assert "Alcohol" in vars(mb.recipes).keys()
    assert "Acid" in vars(mb.recipes).keys()
    assert "Alkane" in vars(mb.recipes).keys()
