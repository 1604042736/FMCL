import os
import shutil


def main():
    if not os.path.exists("../Pack"):
        os.makedirs("../Pack")
    for i in (("Functions", "../FMCL/Functions"),
              ("Translations", "../FMCL/Translations")):
        shutil.make_archive(f"../Pack/{i[0]}Pack", "zip", i[1])
        with open(f"../Pack/{i[0]}.py", mode="w")as file:
            file.write(
                f"""import io
zipfile_bytes=io.BytesIO({open(f'../Pack/{i[0]}Pack.zip',mode='rb').read()})""")


if __name__ == "__main__":
    main()
