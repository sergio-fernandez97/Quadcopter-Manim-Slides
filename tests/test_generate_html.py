from pathlib import Path

from generate_html import (
    build_convert_command,
    get_missing_scene_exports,
    load_scene_order,
)


def test_load_scene_order_uses_slides_toml_order(tmp_path: Path) -> None:
    slides_toml = tmp_path / "slides.toml"
    slides_toml.write_text(
        """
[slides]
slides = [
    "slides.00_intro.IntroSlide",
    "slides.01_methods.MethodsSlide",
    "slides.02_results.ResultsSlide",
]
""".strip(),
        encoding="utf-8",
    )

    assert load_scene_order(slides_toml) == [
        "IntroSlide",
        "MethodsSlide",
        "ResultsSlide",
    ]


def test_get_missing_scene_exports_reports_unrendered_scenes(tmp_path: Path) -> None:
    slides_dir = tmp_path / "slides"
    slides_dir.mkdir()
    (slides_dir / "IntroSlide.json").write_text("{}", encoding="utf-8")

    missing = get_missing_scene_exports(
        ["IntroSlide", "MethodsSlide"],
        slides_dir,
    )

    assert missing == ["MethodsSlide"]


def test_build_convert_command_creates_single_file_offline_export() -> None:
    command = build_convert_command(
        ["IntroSlide", "MethodsSlide"],
        Path("presentation/dissertation_defense.html"),
    )

    assert command == [
        "manim-slides",
        "convert",
        "--to",
        "html",
        "--folder",
        "slides",
        "--one-file",
        "--offline",
        "--config",
        "controls=true",
        "IntroSlide",
        "MethodsSlide",
        "presentation/dissertation_defense.html",
    ]
