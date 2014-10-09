from Bio.Blast import (
    NCBIWWW,
    NCBIXML,
)
import cStringIO


def blast_offtarget(fasta_string):
    """
    Function which count offtarget using blast.
    :param fasta_string: Fasta sequence.
    :type fasta_string: str.
    :returns: int.
    """
    result_handle = NCBIWWW.qblast(
        "blastn", "refseq_rna", fasta_string, entrez_query="txid9606 [ORGN]",
        expect=100, gapcosts="5 2", genetic_code=1, hitlist_size=100,
        word_size=len(fasta_string), megablast=True
    )
    blast_results = result_handle.read()
    blast_in = cStringIO.StringIO(blast_results)
    count = 0

    for record in NCBIXML.parse(blast_in):
        for align in record.alignments:
            count += 1
    return count
