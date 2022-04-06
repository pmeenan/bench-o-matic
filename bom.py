#!/usr/bin/env python3
import logging
import psutil
import sys
import time
from selenium import webdriver
from time import monotonic

class BenchOMatic():
    """Automate browserbench.org testing across browsers using webdriver"""
    def __init__(self, options):
        self.driver = None

    def run(self):
        """Run the requested tests"""
        logging.info('Launching browser...')
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(600)
        self.driver.set_script_timeout(30)
        self.driver.get('https://browserbench.org/Speedometer2.0/')
        self.wait_for_idle()
        logging.info('Starting benchmark...')
        self.driver.execute_script('startTest();')

        # Wait up to 10 minutes for the benchmark to run
        done = False
        end_time = monotonic() + 600
        while not done and monotonic() < end_time:
            time.sleep(2)
            result = self.driver.execute_script("return (document.getElementById('results-with-statistics') && document.getElementById('results-with-statistics').innerText.length > 0);")
            if result:
                done = True

        # Get the benchmark result
        if done:
            result = self.driver.execute_script("return parseInt(document.getElementById('result-number').innerText);")
            confidence = self.driver.execute_script("return parseFloat(document.getElementById('confidence-number').innerText.substring(2))")
            print('Speedometer runs per minute: {}'.format(result))
            print('Confidence: ± {}'.format(confidence))
        else:
            logging.info('Benchmark failed')
        self.driver.quit()

    def wait_for_idle(self, timeout=30):
        """Wait for the system to go idle for at least 2 seconds"""
        logging.info("Waiting for Idle...")
        cpu_count = psutil.cpu_count()
        if cpu_count > 0:
            # No single core more than 30% or 10% total, whichever is higher
            target_pct = max(30. / float(cpu_count), 10.)
            idle_start = None
            end_time = monotonic() + timeout
            last_update = monotonic()
            idle = False
            while not idle and monotonic() < end_time:
                check_start = monotonic()
                pct = psutil.cpu_percent(interval=0.5)
                if pct <= target_pct:
                    if idle_start is None:
                        idle_start = check_start
                    if monotonic() - idle_start > 2:
                        idle = True
                else:
                    idle_start = None
                if not idle and monotonic() - last_update > 1:
                    last_update = monotonic()
                    logging.info("CPU Utilization: %0.1f%% (%d CPU's, %0.1f%% target)", pct, cpu_count, target_pct)

if '__main__' == __name__:
    import argparse
    parser = argparse.ArgumentParser(description='Bench-o-matic', prog='bom')
    parser.add_argument('-v', '--verbose', action='count',
                        help="Increase verbosity (specify multiple times for more). -vvvv for full debug output.")
    options, _ = parser.parse_known_args()

    # Set up logging
    log_level = logging.CRITICAL
    if options.verbose is not None:
      if options.verbose == 1:
          log_level = logging.ERROR
      elif options.verbose == 2:
          log_level = logging.WARNING
      elif options.verbose == 3:
          log_level = logging.INFO
      elif options.verbose >= 4:
          log_level = logging.DEBUG
    logging.basicConfig(
        level=log_level, format="%(asctime)s.%(msecs)03d - %(message)s", datefmt="%H:%M:%S")

    # Kick off the actual benchmarking
    bom = BenchOMatic(options)
    bom.run()