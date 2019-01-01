def read_txt(path):
    """Read a mass spectrum from a text file.
    
    Args:
        path (str): Path to the spectrum.
    
    Returns:
        tuple: Lists with m/z and intensities.
    """
    mz = []
    i = []
    with open(path) as f:
        for line in f:
            line = line.split()
            mz.append(float(line[0]))
            i.append(float(line[1]))
    return mz, i

