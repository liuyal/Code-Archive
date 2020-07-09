import os, sys, time, logging

# https://docs.python.org/2/library/logging.html

def cslog(msg, flag="info"):
    if input_arg.verbose and flag == "info": print(msg)
    elif input_arg.verbose and flag == "error": print("\033[91m" + msg + "\033[0m")
    if input_arg.log:
        if flag == "info": logging.info(msg)
        if flag == "error": logging.error(msg)
        if flag == "critical": logging.critical(msg)
        if flag == "warning": logging.warning(msg)
        if flag == "debug": logging.debug(msg)


if __name__ == "__main__":

	logging.basicConfig(filename="./logging_test.log", filemode='a', format='%(asctime)s, [%(levelname)s] %(name)s, %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
	logging.info("Test Log info")
	logging.error("Test Log ERROR")
	logging.warning("Test Log warning")

	cslog("Logger Test", "info")