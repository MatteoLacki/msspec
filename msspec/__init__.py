try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None


try:
    import plotly
except ModuleNotFoundError:
    plotly = None


print('Setting matplotlib style to dark.')
plt.style.use('dark_background')