# -*- coding: utf-8 -
import traceback


def run_tests(tests):
    """
    Executes the list of functions as argument and keeps track of successful calls. If a function call throws an
    exception, the stacktrack is printed

    :param: tests: Array of functions to be executed
    """
    print "--- STARTING TESTS ---\n"

    count = 0
    for test in tests:
        try:
            test()
            count += 1
            print "Passed ", test.__name__
        except Exception as e:
            print "\tError on test: ", count, ":", test.__name__
            traceback.print_exc()

    print "\nPassed", count, "tests out of", len(tests)
    print "--- END OF TESTS ---"