import asyncio
import aiofiles
import random
import os


async def preprocess_tex(tex, mode="equation"):  # allowed modes: "equation", "document", "tex"
    header = ""
    footer = ""

    if mode == "equation":
        header = """\\documentclass[preview]{standalone}
\\begin{document}
\\["""
        footer = """\\]
\\end{document}"""
    elif mode == "document":
        header = """\\documentclass[preview]{standalone}\\begin{document}"""
        footer = """\\end{document}"""
    elif mode == "tex":
        header = """\\documentclass[preview]{standalone}"""

    return header + '\n' + tex + '\n' + footer


async def save_tex(tex, filen):
    filen = BIN_FOLDER + filen + ".tex"

    #async with aiofiles.open(filen, mode='w') as tex_file:
    #    print(filen)
    #    await tex_file.write(tex)

    with open(filen, 'w') as tex_file:
        tex_file.write(tex)

    return



BIN_FOLDER = os.path.dirname(__file__) + "/bin/"
FILENAME_LENGTH = 30

DENSITY = 300
QUALITY = 90


def clear_bin():
    folder = BIN_FOLDER
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


clear_bin()


def generate_file_name():
    return '%0x' % random.getrandbits(FILENAME_LENGTH * 4)


RENDER_TIMEOUT = 3


class TexRendered:
    def __init__(self, failed=False, prefix="", reason="Unknown render failure"):
        self.failed = failed
        self.reason = reason

        if not failed:
            self.prefix = prefix

    def close(self):
        if not self.failed:
            os.remove(self.img_path())

    def img_path(self):
        return self.prefix + ".jpg"


async def render_tex(filen):
    prefix = BIN_FOLDER + filen

    command = """
        pdflatex -halt-on-error -file-line-error -output-directory {folder} {prefix}.tex | grep ".*:[0-9]*:.*" | sed "s/\(^.*$\)/render-\\1/"
        rm {prefix}.tex {prefix}.aux rm {prefix}.log
        
        if [ ! -f {prefix}.pdf ]; then
            exit 1
        fi
        
        pdfcrop {prefix}.pdf
        rm {prefix}.pdf
        convert -density {DENSITY} {prefix}-crop.pdf -quality {QUALITY} {prefix}.jpg
        rm {prefix}-crop.pdf
        """.format(folder=BIN_FOLDER,
                   DENSITY=DENSITY,
                   QUALITY=QUALITY,
                   prefix=prefix)

    render_process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE)

    try:
        stdout, stderror = await asyncio.wait_for(render_process.communicate(), RENDER_TIMEOUT)
    except TimeoutError as e:
        render_process.terminate()
        return TexRendered(True, prefix, "Rendering LaTeX timed out")

    if render_process.returncode == 0:
        return TexRendered(False, prefix, "Successful LaTeX render")
    else:
        return TexRendered(True, prefix, stdout.decode())


async def render_tex_all(tex_content, mode="equation"):
    name = generate_file_name()

    tex = await preprocess_tex(tex_content, mode)
    await save_tex(tex, name)
    return await render_tex(name)



