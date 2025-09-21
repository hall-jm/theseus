# Theseus

**Governance tools for preserving architectural intent when AI writes the code.**

As artificial intelligence becomes a larger part of software development, maintaining alignment between human architectural decisions and machine-generated implementation becomes critical. Theseus provides systematic governance frameworks that enforce coherence between specifications and implementation, preventing the drift that occurs when intent and code evolve separately.

## What Are ADRs?

Architecture Decision Records (ADRs) are documents that capture important architectural decisions along with their context and consequences. They serve as the bridge between high-level architectural intent and specific implementation choices. While not universally adopted, ADRs provide a structured way to maintain architectural reasoning as systems evolve.

## The Problem

When AI assists with refactoring, feature development, and system changes, subtle inconsistencies compound over time:

- Broken cross-references between documents
- Policy violations that manual review misses
- Structural decay in documentation
- Drift between stated intent and actual implementation

These issues undermine system coherence and make architectural reasoning unreliable.

## Installation

```bash
git clone https://github.com/hall-jm/theseus
cd theseus

python -m venv .venv_theseus
source .venv_theseus/bin/activate   # Windows: .venv_theseus\Scripts\activate

pip install -e .[dev,test]
```

## Usage

```bash
# Validate all ADRs in directory
theseus

# Check specific files
theseus -k 0001
```

## Example Output

**Meta data mismatch between front matter and tail**

```bash
$ theseus -k 0001
Summary: total=1  E=0  W=1  I=0

docs/adrs/ADR-0001-style-guide.md
[W] ADR-META-151: tail mismatch: class, ownership
```

## What It Validates

Theseus enforces structural consistency across multiple dimensions:

**Delta Semantics** - Override target validation, dependency resolution, change tracking
**Link Integrity** - Cross-document references, bidirectional supersede relationships, pointer validation  
**Normative Language** - RFC-2119 keyword placement, vague term detection in requirements
**Schema Validation** - Required metadata, canonical section ordering, class-specific constraints
**Template Compliance** - Section mirroring, placeholder usage, inheritance rules

## Current Status

This is early-stage research focused on systematic governance patterns for AI-assisted development. The tool currently validates ADR documents according to a design specification but should be considered experimental.

## Configuration

Theseus expects ADR files to follow a specific structure defined in the included style guide (`docs/adrs/ADR-0001-style-guide.md`). The tool validates:

- YAML front-matter structure
- Canonical section markers
- Cross-document link integrity
- Policy compliance

## Testing

```bash
# Run the test suite
pytest -q

# Tests include validation of governance rules
# and systematic coverage verification
```

## Research Context

This project emerges from research into sustainable patterns for human-AI collaboration in software development. As teams increasingly work alongside AI tools, systematic governance becomes essential infrastructure for maintaining architectural coherence.

Theseus provides reference implementations and testing patterns for the fundamental challenge of preserving intent through continuous change.

## Contributing

This is primarily a research project exploring governance frameworks for AI-assisted development. Issues and pull requests are welcome, particularly around:

- Validation rule improvements
- Better error reporting
- Documentation clarity
- Integration patterns

## License

This project is dual-licensed under:

- CC-BY-NC-4.0: the ADRS in `docs/adrs`
- Apache-2.0: everything else (e.g., source code)

See LICENSE file for details.
