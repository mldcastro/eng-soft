import argparse
import pathlib
import subprocess


_OUTPUT_IMAGE_DIR = pathlib.Path(__file__).absolute().parent.parent.parent / "diagrams/images"


def convert_to_image(mermaid_file_path: pathlib.Path) -> None:
    _OUTPUT_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    output_image_path = _OUTPUT_IMAGE_DIR / mermaid_file_path.name.replace(
        ".mmd", ".png"
    )

    try:
        _ = subprocess.run(
            [
                "mmdc",
                "-i",
                str(mermaid_file_path.absolute()),
                "-o",
                str(output_image_path),
                "-s",
                "3"
            ],
            capture_output=True,
            check=True,
        )
        print(f"'{mermaid_file_path}' converted to image at '{output_image_path}'.")
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode("utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="Mermaid Image Converter")
    parser.add_argument("-f", "--file", type=pathlib.Path, help="Path to .mmd file.")

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    convert_to_image(args.file)
