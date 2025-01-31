import click
import os
from typing import Optional
from types import SimpleNamespace

from uceasy import __version__
from uceasy.run import run_quality_control, run_assembly, run_alignment


THREADS = os.cpu_count()


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__)
def cli():
    """A unified CLI for the PHYLUCE software package."""
    pass


@cli.command()
@click.argument("raw-fastq", required=True)
@click.argument("csv-file", required=True)
@click.option(
    "--threads",
    "-j",
    type=int,
    default=THREADS,
    help="Number of computer threads to use. (default: all available)",
)
@click.option(
    "--min-len",
    "-m",
    type=int,
    default=40,
    help="The minimum length of reads to keep. (default: 40)",
)
@click.option("--log-dir", "-l", type=str, default=os.getcwd(), help="Directory to save logs.")
@click.option(
    "--output",
    "-o",
    default="clean-fastq",
    help="Output directory. (default: clean-fastq)",
)
@click.option("--r1-pattern", "--r1", help="An optional regex pattern to find R1 reads.")
@click.option("--r2-pattern", "--r2", help="An optional regex pattern to find R2 reads.")
@click.option(
    "--phred64",
    "-p",
    is_flag=True,
    help="Use phred64 for fastq encoding. (default: phred33)",
)
@click.option("--single-end", "--se", is_flag=True, help="Single-end reads.")
@click.option("--single-index", "--si", is_flag=True, help="Single-indexed for barcodes.")
@click.option(
    "--no-merge",
    "-n",
    is_flag=True,
    help="When trimming PE reads, do not merge singleton files.",
)
@click.option("--tracking-file", "-t", default="tracking.csv", help="Provenance tracking file.")
def trim(
    raw_fastq: str,
    csv_file: str,
    threads: int,
    single_end: bool,
    single_index: bool,
    log_dir: str,
    r1_pattern: Optional[str],
    r2_pattern: Optional[str],
    phred64: bool,
    output: str,
    min_len: int,
    no_merge: bool,
    tracking_file: str,
) -> None:
    """Trim adapter sequences with illumiprocessor."""
    context = SimpleNamespace(
        raw_fastq=raw_fastq,
        csv_file=csv_file,
        threads=threads,
        single_end=single_end,
        single_index=single_index,
        log_dir=log_dir,
        r1_pattern=r1_pattern,
        r2_pattern=r2_pattern,
        phred64=phred64,
        output=output,
        min_len=min_len,
        no_merge=no_merge,
        capture_output=True,
        tracking_file=tracking_file,
    )
    run_quality_control(context)


@cli.command()
@click.argument("clean-fastq", required=True)
@click.option(
    "--assembler",
    "-a",
    type=str,
    default="spades",
    help="""Assembler program to use. Available: spades, trinity, velvet and abyss. \
(default: spades)""",
)
@click.option(
    "--config",
    "-c",
    type=str,
    help="Custom configuration file containing the reads to assemble.",
)
@click.option("--kmer", "-k", type=str, help="The kmer value to use.")
@click.option("--log-dir", "-l", type=str, default=os.getcwd(), help="Directory to save logs.")
@click.option(
    "--threads",
    "-j",
    type=int,
    default=THREADS,
    help="Number of computer threads to use. (default: all available)",
)
@click.option(
    "--output",
    "-o",
    type=str,
    default="assemblies",
    help="Output directory. (default: assemblies)",
)
@click.option("--no-clean", "-n", is_flag=True, help="Do not clean intermediate files.")
@click.option(
    "--subfolder",
    "-s",
    type=str,
    help="A subdirectory, below the level of the group, containing the reads.",
)
@click.option("--tracking-file", "-t", default="tracking.csv", help="Provenance tracking file.")
@click.option("--abyss-se", is_flag=True, help="Use only abyss-se.")
@click.option(
    "--min-kmer-coverage",
    type=str,
    help="Sensitivity for reconstructing lowly expressed transcripts. (trinity only)",
)
def assemble(
    assembler: str,
    clean_fastq: str,
    log_dir: str,
    threads: int,
    output: str,
    config: Optional[str],
    kmer: Optional[str],
    min_kmer_coverage: Optional[str],
    no_clean: bool,
    subfolder: Optional[str],
    tracking_file: str,
    abyss_se: bool,
) -> None:
    """Run assembly with spades, trinity, abyss or velvet."""
    context = SimpleNamespace(
        assembler=assembler,
        clean_fastq=clean_fastq,
        log_dir=log_dir,
        threads=threads,
        output=output,
        config=config,
        kmer=kmer,
        min_kmer_coverage=min_kmer_coverage,
        no_clean=no_clean,
        subfolder=subfolder,
        capture_output=True,
        tracking_file=tracking_file,
        abyss_se=abyss_se,
    )
    run_assembly(context)


@cli.command()
@click.argument("contigs", required=True)
@click.argument("probes", required=True)
@click.option(
    "--aligner",
    "-a",
    type=str,
    default="mafft",
    help="Aligner program to use. Available: mafft, muscle. (default: mafft)",
)
@click.option("--charsets", "-c", is_flag=True, help="Use charsets.")
@click.option(
    "--threads",
    "-j",
    type=int,
    default=THREADS,
    help="Number of computer threads to use. (default: all available)",
)
@click.option(
    "--output",
    "-o",
    type=str,
    default="alignments",
    help="Output directory. (default: alignments)",
)
@click.option("--incomplete-matrix", is_flag=True, help="Generate an incomplete matrix of data.")
@click.option("--internal-trimming", "-i", is_flag=True, help="Internally trim the alignments.")
@click.option("--log-dir", "-l", type=str, default=os.getcwd(), help="Directory to save logs.")
@click.option(
    "--regex",
    "-r",
    help="A regular expression to apply to the probe names for replacement.",
)
@click.option(
    "--percent",
    "-p",
    default=0.75,
    help="The percent of taxa to require (default: 0.75)",
)
@click.option("--tracking-file", "-t", default="tracking.csv", help="Provenance tracking file.")
@click.option("--phylip", is_flag=True, help="Use phylip format for the final concatenated data.")
def align(
    aligner: str,
    charsets: bool,
    contigs: str,
    incomplete_matrix: bool,
    internal_trimming: bool,
    output: str,
    log_dir: str,
    probes: str,
    percent: float,
    threads: int,
    regex: Optional[str],
    tracking_file: str,
    phylip: bool,
):
    """Alignment and extraction of UCE data."""
    context = SimpleNamespace(
        aligner=aligner,
        charsets=charsets,
        contigs=contigs,
        incomplete_matrix=incomplete_matrix,
        internal_trimming=internal_trimming,
        output=output,
        log_dir=log_dir,
        probes=probes,
        percent=percent,
        threads=threads,
        regex=regex,
        capture_output=True,
        tracking_file=tracking_file,
        phylip=phylip,
    )
    run_alignment(context)
