# d-LIN reading and seminar materials

Revised 5 October 2026. These materials explain the sparse noisy linear problem studied by Applebaum, Barak and Wigderson (ABW), its hardness assumptions, its comparison with LPN, LWE and Module-LWE, and the benefits and limitations of using it for public-key encryption.

## Suggested reading order

1. **Student presentation:** a 24-slide introduction to parity equations, noise, the computational tasks, and the ABW encryption idea.
2. **`my_notes/dLIN/drafts/understanding-dlin-through-abw09-draft.tex`:** the detailed notes, with equations, worked examples, precise assumptions, comparisons, exercises, and source references. Open or compile this editable LaTeX source to read the full document.
3. **Expert seminar:** a 24-slide treatment of ABW's theorem hypotheses, reductions, hidden dependencies, correctness, amplification, and the limits of the hardness evidence.
4. **Error-count comparison:** three binomial distributions for 20 equations and noise probabilities 0.5, 0.25, and 0.7. These are illustrative examples, not proposed encryption parameters. The revised expert presentation includes this comparison on slide 06.

## Files and formats

| Material | Formats | Use |
|---|---|---|
| Revised notes | `../my_notes/dLIN/drafts/understanding-dlin-through-abw09-draft.tex` | Editable source and full references |
| Student presentation | `day01-experiment/slides/dlin-student-edition.pptx` and `day01-experiment/slides/student-edition-abw-revised.pdf` | Introductory teaching |
| Expert seminar | `day01-experiment/slides/dlin-expert-seminar.pptx` and `day01-experiment/slides/expert-seminar-abw-revised.pdf` | Technical seminar and discussion |
| Error-count comparison | `day01-experiment/epsilon-binomial-graphs/error-count-comparison.pptx` and `day01-experiment/epsilon-binomial-graphs/error-count-comparison.png` | Editable graph slide and quick viewing image |
| Graph data | `day01-experiment/epsilon-binomial-graphs/error-count-probabilities.csv` | Exact binomial probabilities for counts 0 to 20 |
| This guide | `README.md` | File inventory and reading order |

The PowerPoints retain editable text, tables, and charts, with citations and explanations in their speaker notes. The slide PDFs are high-resolution visual copies with slide bookmarks. They preserve the presentation appearance but do not contain selectable slide text or speaker notes. Use the PowerPoint files for editing and for access to speaker notes.

## Main distinctions to keep in mind

- The sampled matrix distribution, noise rate, number of equations, and recovery or distinguishing goal are part of a hardness assumption.
- Sparse d-LIN, dense LPN, LWE, and Module-LWE share a noisy linear template but make different distributional and algebraic assumptions.
- ABW proves conditional, asymptotic public-key encryption results. The paper does not provide a concrete standardized encryption or key-encapsulation parameter set.
- Restricted attack lower bounds support study of the assumption without proving hardness against every efficient adversary.

## Primary sources

- [Applebaum, Barak and Wigderson, Public-Key Cryptography from Different Assumptions (7 November 2009 manuscript)](https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/ABW09/ABW09.pdf). The notes use this manuscript's theorem and section numbering.
- [Regev, On Lattices, Learning with Errors, Random Linear Codes, and Cryptography](https://cims.nyu.edu/~regev/papers/qcrypto.pdf).
- [Langlois and Stehlé, Worst-case to average-case reductions for module lattices](https://perso.ens-lyon.fr/damien.stehle/downloads/MSIS.pdf).
- [NIST FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).
- [Kiltz, Masny and Pietrzak, Simple Chosen-Ciphertext Security from Low-Noise LPN](https://eprint.iacr.org/2015/401).
- [Yu and Zhang, Cryptography with Auxiliary Input and Trapdoor from Constant-Noise LPN](https://www.iacr.org/archive/crypto2016/98140212/98140212.pdf).

The notes and presentations are based on Prajjwal Saxena's notes and were revised with the assistance of GPT. Consult the original papers for formal statements and proofs.
