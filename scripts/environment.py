import os


def exitError(message, exitCode=1):
    print(message)
    exit(exitCode)


def env(key, default=None):
    return os.getenv(key, default)


def require(name):
    value = env(name)

    if value is None:
        return exitError("The environment variable '%s' is required" % (name,))

    return value
