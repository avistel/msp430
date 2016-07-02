import SCons.Tool.cc as cc
import SCons.Util
import subprocess
import re

def generate(env):
    """Add Builders and construction variables for gcc to an Environment. """
    cc.generate(env)
    env['CC'] = env.Detect('msp430-gcc')
    env['CXX'] = env.Detect('msp430-g++')
    env['LINK'] = env.Detect('msp430-g++')
    env['AS'] = env.Detect('msp430-as')
    env['AR'] = env.Detect('msp430-ar')
    env['RANLIB'] = env.Detect('msp430-ranlib')

    if env['PLATFORM'] in ['cygwin', 'win32']:
        env['SHCCFLAGS'] = SCons.Util.CLVar('$CCFLAGS')
    else:
        env['SHCCFLAGS'] = SCons.Util.CLVar('$CCFLAGS -fPIC')
    # determine compiler version
    if env['CC']:
        #pipe = SCons.Action._subproc(env, [env['CC'], '-dumpversion'],
        pipe = SCons.Action._subproc(env, [env['CC'], '--version'],
                                     stdin = 'devnull',
                                     stderr = 'devnull',
                                     stdout = subprocess.PIPE)
        if pipe.wait() != 0: return
        # -dumpversion was added in GCC 3.0.  As long as we're supporting
        # GCC versions older than that, we should use --version and a
        # regular expression.
        #line = pipe.stdout.read().strip()
        #if line:
        #    env['CCVERSION'] = line
        line = pipe.stdout.readline()
        match = re.search(r'[0-9]+(\.[0-9]+)+', line)
        if match:
            env['CCVERSION'] = match.group(0)


def exists(env):
    # is executable, and is a GNU compiler (or accepts '--version' at least)
    return env.Detect('msp430-gcc')
