def pytest_addoption(parser):
    parser.addoption('--mock-use', default=False, help='set True to test by mock. default is False.')
