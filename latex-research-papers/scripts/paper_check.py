#!/usr/bin/env python3
"""Compile a LaTeX paper with Tectonic and report layout, reference, citation, and link problems.

Usage: python paper_check.py main.tex [--tectonic PATH] [--outdir DIR] [--allow REGEX]...
                             [--render DIR] [--check-links]
Exits 1 when anything blocking remains: TeX errors, overfull boxes, missing glyphs,
undefined or duplicate labels, BibTeX warnings, missing or uncited bibliography
entries, book or preprint entries (book types, arXiv, bioRxiv, medRxiv, SSRN,
eprint), unreferenced or unlabelled figures and tables, numeric citations out of
order of first appearance, no hyperref, and (when pypdf is installed) '??' in the
PDF, cited DOIs or URLs that are not links in the PDF, or figures and tables more
than one page after their first mention.
Labels of a document named by \externaldocument (xr or xr-hyper, for example a separate
supplementary PDF) are valid \ref targets, read from its .aux next to the main file, and
a bibliography entry cited only by that document is not reported as uncited.
--allow downgrades log or BibTeX lines matching REGEX (for example a
template-internal overfull box already checked in the PDF) to accepted.
Figures and tables in the appendix are exempt from the placement check. Underfull boxes and other
warnings are listed but never fail the check.
PDF checks need pypdf; --render also needs pypdfium2. Without them they are skipped.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

LOG_PATTERNS = {
    "error": re.compile(r"^! .*"),
    "overfull": re.compile(r"^Overfull \\[hv]box .*"),
    "underfull": re.compile(r"^Underfull \\[hv]box .*"),
    "missing_char": re.compile(r"^Missing character: .*"),
    "warning": re.compile(
        r"^(?:LaTeX|Package|Class) [\w-]* ?Warning: .*|^LaTeX Font Warning: .*"
    ),
}
BLOCKING_WARNINGS = re.compile(
    r"undefined|multiply defined|Float too large|There were undefined|Rerun to get|"
    r"destination with the same identifier",
    re.IGNORECASE,
)
REF_COMMANDS = r"\\(?:[cC]ref|[vV]ref|autoref|ref|eqref|pageref|nameref|cpageref|labelcref)\*?\{([^}]+)\}"


def repo_root(start: Path) -> Path | None:
    for folder in [start, *start.parents]:
        if (folder / ".git").exists():
            return folder
    return None


def find_tectonic(explicit: str | None, tex: Path) -> Path:
    if explicit or os.environ.get("TECTONIC"):
        return Path(explicit or os.environ["TECTONIC"])
    on_path = shutil.which("tectonic")
    if on_path:
        return Path(on_path)
    for folder in [tex.parent, *tex.parent.parents]:
        for name in ("tectonic.exe", "tectonic"):
            candidates = [
                p for p in [folder / name, *folder.glob(f"*/{name}")] if p.is_file()
            ]
            if candidates:
                return candidates[0]
    raise SystemExit(
        "tectonic not found: pass --tectonic PATH, set TECTONIC, or install it into the project (see references/fixes.md, Install Tectonic)."
    )


def compile_paper(tectonic: Path, tex: Path, outdir: Path, root: Path) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    # A fixed rerun count: Tectonic 0.15's automatic .bbl check otherwise loops to
    # its six-pass limit after the document has converged.
    cmd = [
        str(tectonic),
        "--keep-logs",
        "--keep-intermediates",
        "--reruns",
        "3",
        "--outdir",
        str(outdir),
        str(tex),
    ]
    env = {**os.environ}
    env.setdefault("TECTONIC_CACHE_DIR", str(root / ".cache" / "tectonic"))
    print("$ " + " ".join(cmd))
    print(f"  TECTONIC_CACHE_DIR={env['TECTONIC_CACHE_DIR']}")
    result = subprocess.run(
        cmd,
        cwd=tex.parent,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode:
        print(result.stdout[-4000:])
        print(result.stderr[-4000:])
    return result.returncode


def joined_log_lines(log: str) -> list[str]:
    """TeX wraps log lines at 79 characters; rejoin them so messages stay whole."""
    lines, current = [], ""
    for raw in log.splitlines():
        current += raw
        if len(raw) != 79:
            lines.append(current)
            current = ""
    if current:
        lines.append(current)
    return lines


def scan_log(log: str) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {key: [] for key in LOG_PATTERNS}
    lines = joined_log_lines(log)
    for index, line in enumerate(lines):
        for key, pattern in LOG_PATTERNS.items():
            if pattern.match(line):
                detail = line
                if key in ("overfull", "underfull", "error") and index + 1 < len(lines):
                    detail += "  >> " + lines[index + 1].strip()[:120]
                found[key].append(detail)
    return found


def strip_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", text)


def source_files(tex: Path) -> list[Path]:
    """The main file plus every \\input or \\include it reaches."""
    seen, queue = [], [tex]
    while queue:
        path = queue.pop()
        if path in seen or not path.exists():
            continue
        seen.append(path)
        text = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        for name in re.findall(r"\\(?:input|include|subfile)\{([^}]+)\}", text):
            child = tex.parent / name
            queue.append(child if child.suffix == ".tex" else child.with_suffix(".tex"))
    return seen


def read_aux(outdir: Path, stem: str, includes: set[str]) -> str:
    """Main .aux first, then those of \\include files, so citation order is preserved.

    Only included files count: another document's .aux in the same build folder (for
    example a supplement built there earlier) must not leak into this one.
    """
    main = outdir / f"{stem}.aux"
    others = [
        p for p in sorted(outdir.glob("*.aux")) if p != main and p.stem in includes
    ]
    return "\n".join(
        p.read_text(encoding="utf-8", errors="replace")
        for p in [main, *others]
        if p.exists()
    )


def bib_keys(
    aux: str, tex_dir: Path, sources: str
) -> tuple[dict[str, str], list[Path]]:
    names = []
    for group in re.findall(r"\\bibdata\{([^}]+)\}", aux):
        names += group.split(",")
    names += re.findall(r"\\addbibresource(?:\[[^]]*\])?\{([^}]+)\}", sources)
    files = []
    for name in dict.fromkeys(n.strip() for n in names if n.strip()):
        path = tex_dir / (name if name.endswith(".bib") else name + ".bib")
        if path.exists():
            files.append(path)
    entries: dict[str, str] = {}
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
            if match.group(1).lower() not in ("string", "preamble", "comment"):
                end = text.find("\n@", match.end())
                entries[match.group(2)] = text[
                    match.start() : end if end > 0 else len(text)
                ]
    return entries, files


def cited_in_order(aux: str) -> tuple[list[str], bool]:
    keys, cite_all = [], False
    for group in re.findall(
        r"\\citation\{([^}]+)\}|\\abx@aux@cite\{[^}]*\}\{([^}]+)\}", aux
    ):
        for key in ",".join(g for g in group if g).split(","):
            key = key.strip()
            if key == "*":
                cite_all = True
            elif key and key not in keys:
                keys.append(key)
    return keys, cite_all


def bib_numbers(aux: str) -> dict[str, str]:
    numbers = {}
    for key, value in re.findall(
        r"\\bibcite\{([^}]+)\}\{(.*)\}\s*$", aux, re.MULTILINE
    ):
        inner = re.match(r"\{([^{}]*)\}", value)
        numbers[key] = (inner.group(1) if inner else value).strip()
    return numbers


def is_author_year(sources: str) -> bool:
    """natbib defaults to author-year unless the numbers or super option is set."""
    biblatex = re.search(r"\\usepackage\[([^]]*)\]\{biblatex\}", sources)
    if biblatex:
        return bool(re.search(r"style=(?:authoryear|apa|chicago)", biblatex.group(1)))
    natbib = re.search(r"\\usepackage(?:\[([^]]*)\])?\{[^}]*natbib[^}]*\}", sources)
    numeric = re.search(
        r"\\(?:setcitestyle|biboptions)\{[^}]*(?:numbers|super)", sources
    )
    return (
        bool(natbib)
        and not numeric
        and not re.search(r"numbers|super", natbib.group(1) or "")
    )


def float_entries(aux: str) -> list[tuple[str, str, str, str]]:
    """(kind, number, page, anchor) for every captioned figure and table, from the .lof/.lot lines."""
    pattern = r"\\contentsline \{(figure|table)\}\{\\numberline \{([^}]*)\}.*\}\{([^{}]*)\}\{([^{}]*)\}"
    return re.findall(pattern, aux)


def label_anchors(aux: str) -> dict[str, str]:
    """label -> hyperref anchor, read from \\newlabel{key}{{num}{page}{title}{anchor}{}}."""
    anchors = {}
    for key, body in re.findall(
        r"\\newlabel\{([^}]+)\}\{(.*)\}\s*$", aux, re.MULTILINE
    ):
        fields = re.findall(r"\{((?:[^{}]|\{[^{}]*\})*)\}", body)
        anchors[key] = fields[3] if len(fields) > 3 else ""
    return anchors


def appendix_page(aux: str) -> str | None:
    """Page label where the appendix starts; its figures and tables may sit far from a body mention."""
    match = re.search(
        r"\\contentsline \{\w+\}.*\}\{([^{}]*)\}\{appendix\.[^{}]*\}", aux
    )
    return match.group(1) if match else None


def bib_targets(entries: dict[str, str], cited: list[str]) -> dict[str, str]:
    """key -> the DOI (or else URL) each cited entry should link to in the PDF."""
    targets = {}
    for key in cited:
        body = entries.get(key, "")
        doi = re.search(r"[,\s]doi\s*=\s*[{\"]\s*([^}\"\s]+)", body, re.IGNORECASE)
        url = re.search(r"[,\s]url\s*=\s*[{\"]\s*([^}\"\s]+)", body, re.IGNORECASE)
        if doi or url:
            targets[key] = (doi or url).group(1).lower().rstrip("/")
    return targets


def pdf_checks(
    pdf: Path,
    floats: list[tuple[str, str, str, str]],
    appendix: str | None,
    targets: dict[str, str],
    render: Path | None,
    check_links: bool,
) -> tuple[list[str], list[str], list[str]]:
    """Returns (report lines, blocking problems, placement issues). Needs pypdf."""
    try:
        from pypdf import PdfReader
    except ImportError:
        return (
            ["PDF checks skipped: pypdf is not installed in this environment."],
            [],
            [],
        )
    reader = PdfReader(str(pdf))
    texts = [page.extract_text() or "" for page in reader.pages]
    report, problems, placement = [f"Pages: {len(texts)}"], [], []

    unresolved = [str(i + 1) for i, text in enumerate(texts) if "??" in text]
    report.append(f"Pages containing '??': {', '.join(unresolved) or 'none'}")
    if unresolved:
        problems.append("'??' in the PDF (unresolved reference or citation)")

    bookmarks = len(reader.outline)
    report.append(f"Top-level PDF bookmarks: {bookmarks}")
    if bookmarks == 0:
        problems.append("PDF has no bookmarks (see references/fixes.md, Bookmarks)")

    labels = list(reader.page_labels)

    def page_index(page: str | None) -> int | None:
        if page is None:
            return None
        return (
            labels.index(page)
            if page in labels
            else (int(page) - 1 if page.isdigit() else None)
        )

    appendix_index = page_index(appendix)
    words = {"figure": r"(?:Figures?|Figs?\.)", "table": r"Tables?"}
    for kind, number, page, _anchor in floats:
        index = page_index(page)
        if index is None or (appendix_index is not None and index >= appendix_index):
            continue
        mention = re.compile(
            rf"{words[kind]}\s*(?:[\w.]+\s*(?:,|and|to|–|-)\s*)*{re.escape(number)}(?![\w.]*\d)"
        )
        first = next((i for i, text in enumerate(texts) if mention.search(text)), index)
        if index - first > 1:
            placement.append(
                f"{kind} {number} is on page {index + 1}, first mentioned on page {first + 1}"
            )

    internal, external = 0, {}
    for page in reader.pages:
        for annot in page.get("/Annots") or []:
            obj = annot.get_object()
            if obj.get("/Subtype") != "/Link":
                continue
            action = obj.get("/A")
            uri = action.get_object().get("/URI") if action is not None else None
            if uri:
                external[str(uri)] = external.get(str(uri), 0) + 1
            else:
                internal += 1
    report.append(
        f"Links: {internal} internal, {sum(external.values())} external ({len(external)} unique)"
    )
    linked = [urllib.parse.unquote(uri).lower().rstrip("/") for uri in external]
    unlinked = [
        f"{key}: {target}"
        for key, target in targets.items()
        if not any(uri.endswith(target) or uri == target for uri in linked)
    ]
    report.append(f"Cited DOIs or URLs not clickable in the PDF: {len(unlinked)}")
    report += [f"  - {item}" for item in unlinked[:40]]
    if unlinked:
        problems.append(
            "Cited DOIs or URLs not clickable in the PDF (style drops or does not link them)"
        )
    if check_links:
        for uri in sorted(external):
            try:
                request = urllib.request.Request(
                    uri, method="HEAD", headers={"User-Agent": "Mozilla/5.0"}
                )
                status = urllib.request.urlopen(request, timeout=30).status
            except Exception as exc:  # report every link, never stop
                status = getattr(exc, "code", type(exc).__name__)
            report.append(f"  [{status}] {uri}")

    if render:
        try:
            import pypdfium2 as pdfium
        except ImportError:
            report.append(
                "Render skipped: pypdfium2 is not installed in this environment."
            )
        else:
            render.mkdir(parents=True, exist_ok=True)
            document = pdfium.PdfDocument(str(pdf))
            for i in range(len(document)):
                document[i].render(scale=1.3).to_pil().save(
                    render / f"page-{i + 1:02d}.png"
                )
            report.append(f"Rendered {len(document)} pages to {render}")
    return report, problems, placement


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("tex", type=Path)
    parser.add_argument("--tectonic")
    parser.add_argument("--outdir", type=Path)
    parser.add_argument("--allow", action="append", default=[], metavar="REGEX")
    parser.add_argument("--render", type=Path, metavar="DIR")
    parser.add_argument("--check-links", action="store_true")
    args = parser.parse_args()

    tex = args.tex.resolve()
    root = repo_root(tex.parent) or tex.parent
    outdir = (args.outdir or root / ".agent-local" / "tmp" / "latex-build").resolve()
    tectonic = find_tectonic(args.tectonic, tex)
    problems: list[str] = []

    if compile_paper(tectonic, tex, outdir, root):
        problems.append("Tectonic failed; fix the first error shown above.")

    log_path = outdir / f"{tex.stem}.log"
    log = (
        log_path.read_text(encoding="utf-8", errors="replace")
        if log_path.exists()
        else ""
    )
    found = scan_log(log)
    allowed = [re.compile(pattern) for pattern in args.allow]
    accepted = [
        line
        for key in ("error", "overfull", "missing_char", "warning")
        for line in found[key]
        if any(p.search(line) for p in allowed)
    ]
    for key in found:
        found[key] = [line for line in found[key] if line not in accepted]
    blocking_warnings = [w for w in found["warning"] if BLOCKING_WARNINGS.search(w)]
    blg_path = outdir / f"{tex.stem}.blg"
    blg = (
        blg_path.read_text(encoding="utf-8", errors="replace")
        if blg_path.exists()
        else ""
    )
    bibtex_warnings = re.findall(r"^Warning--.*|^.*error message.*", blg, re.MULTILINE)
    accepted += [w for w in bibtex_warnings if any(p.search(w) for p in allowed)]
    bibtex_warnings = [w for w in bibtex_warnings if w not in accepted]

    sources_text = "\n".join(
        strip_comments(p.read_text(encoding="utf-8", errors="replace"))
        for p in source_files(tex)
    )
    includes = {
        Path(name).stem for name in re.findall(r"\\include\{([^}]+)\}", sources_text)
    }
    aux = read_aux(outdir, tex.stem, includes)
    cited, cite_all = cited_in_order(aux)
    entries, bib_files = bib_keys(aux, tex.parent, sources_text)
    if re.search(r"\\bibitem", sources_text):
        entries = {
            k: ""
            for k in re.findall(r"\\bibitem(?:\[[^]]*\])?\{([^}]+)\}", sources_text)
        }
    external_labels: set[str] = set()
    external_cited: set[str] = set()
    # \Variant in \externaldocument{main\Variant} is "-anonymised" in the anonymised
    # wrappers and empty otherwise, matching the file being checked.
    variant = "-anonymised" if tex.stem.endswith("-anonymised") else ""
    for prefix, name in re.findall(
        r"\\externaldocument(?:\[([^]]*)\])?\{([^}]+)\}", sources_text
    ):
        name = re.sub(r"\\Variant(?:\{\})?", variant, name)
        ext_aux = tex.parent / f"{name}.aux"
        if ext_aux.exists():
            ext_text = ext_aux.read_text(encoding="utf-8", errors="replace")
            external_labels.update(prefix + k for k in label_anchors(ext_text))
            external_cited.update(cited_in_order(ext_text)[0])
    missing = [k for k in cited if k not in entries]
    uncited = (
        []
        if cite_all
        else [k for k in entries if k not in cited and k not in external_cited]
    )

    numbers = bib_numbers(aux)
    order_note = "skipped (no bibliography numbers in .aux)"
    out_of_order: list[str] = []
    if numbers and is_author_year(sources_text):
        order_note = "skipped (author-year citations; the style orders the list)"
    elif numbers and all(numbers.get(k, "").isdigit() for k in cited if k in numbers):
        in_list = [k for k in cited if k in numbers]
        sequence = [int(numbers[k]) for k in in_list]
        out_of_order = [
            f"{k} is [{numbers[k]}]"
            for k, n, e in zip(in_list, sequence, sorted(sequence))
            if n != e
        ][:10]
        order_note = "ok" if not out_of_order else "out of order"

    anchors = label_anchors(aux)
    referenced = set()
    for group in re.findall(REF_COMMANDS, sources_text):
        referenced.update(k.strip() for k in group.split(","))
    floats = float_entries(aux)
    float_anchors = {anchor for *_rest, anchor in floats}
    float_labels = {k for k, anchor in anchors.items() if anchor in float_anchors}
    unreferenced_floats = sorted(float_labels - referenced)
    labelled_anchors = {anchors[k] for k in float_labels}
    unlabelled_floats = [
        f"{kind} {number}"
        for kind, number, _page, anchor in floats
        if anchor not in labelled_anchors
    ]
    broken_refs = sorted(
        k for k in referenced - set(anchors) - external_labels if "#" not in k
    )

    hyperref = bool(re.search(r"^Package: hyperref", log, re.MULTILINE))
    no_link_entries = [
        k
        for k, body in entries.items()
        if body and not re.search(r"[,\s](doi|url)\s*=", body, re.IGNORECASE)
    ]
    not_peer_reviewed = [
        k
        for k, body in entries.items()
        if re.search(
            r"^@\s*(?:book|inbook|booklet|unpublished)\b"
            r"|arxiv|biorxiv|medrxiv|ssrn|preprint|[,\s]eprint\s*=",
            body,
            re.IGNORECASE,
        )
    ]
    bare_urls = re.findall(
        r"(?<![{=/\w])(https?://[^\s}{]+)",
        re.sub(r"\\(?:url|href)\{[^}]*\}", "", sources_text),
    )
    years = sorted(
        int(y)
        for body in entries.values()
        for y in re.findall(r"[,\s]year\s*=\s*[{\"]?(\d{4})", body, re.IGNORECASE)
    )

    def section(title: str, items: list[str], blocking: bool) -> None:
        print(f"\n{title}: {len(items)}")
        for item in items[:40]:
            print("  - " + item)
        if len(items) > 40:
            print(f"  ... {len(items) - 40} more")
        if blocking and items:
            problems.append(f"{title}: {len(items)}")

    pdf = outdir / f"{tex.stem}.pdf"
    print(f"\nPDF: {pdf}")
    print(f"Log: {log_path}")
    section("Errors", found["error"], True)
    section("Overfull boxes (overflow)", found["overfull"], True)
    section("Missing glyphs", found["missing_char"], True)
    section(
        "Blocking warnings (undefined, duplicate, rerun, float too large)",
        blocking_warnings,
        True,
    )
    section("BibTeX warnings", bibtex_warnings, True)
    section("Broken \\ref targets", broken_refs, True)
    section("Cited but missing from bibliography", missing, True)
    section("Bibliography entries never cited", uncited, True)
    section("Books or preprints in bibliography", not_peer_reviewed, True)
    section("Figures or tables never referenced in text", unreferenced_floats, True)
    section("Figures or tables without a \\label", unlabelled_floats, True)
    print(f"\nCitation order of first appearance: {order_note}")
    for item in out_of_order:
        print("  - " + item)
    if out_of_order:
        problems.append("Citations not numbered in order of first appearance")
    print(f"hyperref loaded: {'yes' if hyperref else 'no'}")
    if not hyperref:
        problems.append("hyperref not loaded; links are not clickable")

    if pdf.exists():
        report, pdf_problems, placement = pdf_checks(
            pdf,
            floats,
            appendix_page(aux),
            bib_targets(entries, cited),
            args.render,
            args.check_links,
        )
        print()
        print("\n".join(report))
        problems += pdf_problems
        section(
            "Figures or tables more than one page after their first mention",
            placement,
            True,
        )

    section("Bibliography entries without doi or url", no_link_entries, False)
    section("Bare URLs outside \\url or \\href", sorted(set(bare_urls)), False)
    if years:
        print(
            f"\nReference years: {years[0]} to {years[-1]}, median {years[len(years) // 2]}"
        )
    section("Underfull boxes", found["underfull"], False)
    section(
        "Other warnings",
        [w for w in found["warning"] if w not in blocking_warnings],
        False,
    )
    section("Accepted by --allow (name each in the final reply)", accepted, False)
    print(
        f"\nBibliography files: {', '.join(str(p) for p in bib_files) or 'none found'}"
    )

    print("\nRESULT: " + ("CLEAN" if not problems else "NOT CLEAN"))
    for problem in problems:
        print("  - " + problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
