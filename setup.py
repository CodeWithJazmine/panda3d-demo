from setuptools import setup

setup(
    name='Panda Attack',
    version='0.1.0',
    options={
        'build_apps': {
            # Build panda attack as a GUI application
            'gui_apps': {
                'Panda Attack': 'main.py',
            },

            #Setup output logging, important for GUI apps
            'log_filename': '$USER_APPDATA/Panda Attack/output.log',
            'log_append': False,

            # Specify which files are included with the distribution
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                'models/*',
            ],

            # Include OpenGL renderer and OpenAL audio plug-in
            'plugins': [
                'pandagl',
            ],
            
            # Specify what platforms to build for
            'platforms': [
                'macosx_10_9_x86_64',
                'win_amd64',
            ],
        }
    }
)