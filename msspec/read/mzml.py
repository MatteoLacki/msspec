from pathlib import Path


def read_mzml(path, scan=None):
    """Read mzXML spectra.

    Generate a sequence of spectra from the path.
    
    Parameters
    ----------
    path : str
        Path to the mass spectrum file (mzxml, mzml, txt).
    Returns
    -------
    tuple : m/z ratios and intensities.
    """
    path = Path(path)
    reader = {'.mzxml': mzxml, '.mzml': mzml}[path.suffix.lower()]
    with reader.read(str(path)) as info:
        for i, spectrum in enumerate(info):
            if scan:
                if i is scan:
                    yield spectrum
            else:
                yield spectrum