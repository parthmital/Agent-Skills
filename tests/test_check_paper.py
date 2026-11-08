import pytest


def test_joined_log_lines_rejoins_79_character_wraps(check_paper):
    first = "x" * 79
    assert check_paper.joined_log_lines(f"{first}\nrest\nnext") == [
        first + "rest",
        "next",
    ]


def test_scan_log_classifies_lines(check_paper):
    log = (
        "! Undefined control sequence.\n"
        "l.12 \\foo\n"
        "Overfull \\hbox (3.0pt too wide) in paragraph at lines 4--5\n"
        "Underfull \\vbox (badness 10000) has occurred\n"
        "LaTeX Warning: Reference `x' on page 1 undefined on input line 3.\n"
        "Missing character: There is no X in font cmr10!\n"
    )
    found = check_paper.scan_log(log)
    assert found["error"][0].startswith("! Undefined") and "l.12" in found["error"][0]
    assert len(found["overfull"]) == len(found["underfull"]) == 1
    assert len(found["missing_char"]) == 1
    assert check_paper.BLOCKING_WARNINGS.search(found["warning"][0])


def test_strip_comments_keeps_escaped_percent(check_paper):
    assert check_paper.strip_comments("50\\% done % note") == "50\\% done "


def test_source_files_follows_inputs_with_dotted_names(check_paper, tmp_path):
    (tmp_path / "main.tex").write_text(
        "\\input{intro.v2}\n\\include{body}\n% \\input{ignored}\n", encoding="utf-8"
    )
    (tmp_path / "intro.v2.tex").write_text("intro", encoding="utf-8")
    (tmp_path / "body.tex").write_text("body", encoding="utf-8")
    names = {path.name for path in check_paper.source_files(tmp_path / "main.tex")}
    assert names == {"main.tex", "intro.v2.tex", "body.tex"}


def test_cited_in_order_and_cite_all(check_paper):
    aux = "\\citation{b,a}\n\\citation{a}\n\\citation{c}\n\\citation{*}\n"
    assert check_paper.cited_in_order(aux) == (["b", "a", "c"], True)


def test_bib_numbers(check_paper):
    aux = "\\bibcite{a}{{1}{2020}{{A}}{{}}}\n\\bibcite{b}{2}\n"
    assert check_paper.bib_numbers(aux) == {"a": "1", "b": "2"}


@pytest.mark.parametrize(
    ("preamble", "author_year"),
    [
        ("\\usepackage{natbib}", True),
        ("\\usepackage[numbers]{natbib}", False),
        ("\\usepackage{natbib}\\setcitestyle{numbers}", False),
        ("\\usepackage[style=apa]{biblatex}", True),
        ("\\usepackage[style=numeric]{biblatex}", False),
        ("", False),
    ],
)
def test_is_author_year(check_paper, preamble, author_year):
    assert check_paper.is_author_year(preamble) is author_year


def test_labels_and_floats(check_paper):
    aux = (
        "\\newlabel{fig:a}{{1}{3}{Cap}{figure.caption.1}{}}\n"
        "\\@writefile{lof}{\\contentsline {figure}{\\numberline {1}{\\ignorespaces Cap}}"
        "{3}{figure.caption.1}}%\n"
    )
    assert check_paper.label_anchors(aux) == {"fig:a": "figure.caption.1"}
    assert check_paper.float_entries(aux) == [("figure", "1", "3", "figure.caption.1")]


def test_bib_targets_prefers_doi(check_paper):
    entries = {
        "a": "@article{a,\n doi = {10.1/ABC},\n url = {https://x.org/a}\n}",
        "b": "@article{b,\n url = {https://x.org/b/}\n}",
        "c": "@article{c,\n title = {T}\n}",
    }
    assert check_paper.bib_targets(entries, ["a", "b", "c"]) == {
        "a": "10.1/abc",
        "b": "https://x.org/b",
    }


def test_bib_keys_skips_string_entries(check_paper, tmp_path):
    (tmp_path / "refs.bib").write_text(
        "@string{j = {J}}\n@article{key1,\n title={A}}\n@inproceedings{key2,\n title={B}}\n",
        encoding="utf-8",
    )
    entries, files = check_paper.bib_keys("\\bibdata{refs}", tmp_path, "")
    assert set(entries) == {"key1", "key2"} and files == [tmp_path / "refs.bib"]


def test_find_tectonic_rejects_missing_explicit_path(check_paper, tmp_path):
    with pytest.raises(SystemExit, match="tectonic not found"):
        check_paper.find_tectonic(str(tmp_path / "nope.exe"), tmp_path / "main.tex")


def test_find_tectonic_finds_binary_in_subfolder(check_paper, tmp_path, monkeypatch):
    monkeypatch.delenv("TECTONIC", raising=False)
    monkeypatch.setattr(check_paper.shutil, "which", lambda _name: None)
    binary = tmp_path / "tools" / "tectonic"
    binary.parent.mkdir()
    binary.write_text("", encoding="utf-8")
    assert check_paper.find_tectonic(None, tmp_path / "main.tex") == binary
