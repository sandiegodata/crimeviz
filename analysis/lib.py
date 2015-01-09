from math import ceil

def plot_heat_grid(df, legends = None, incident_type=None):
    """Plot a heatmap grid"""
    import numpy as np

    if not legends:
        legends = sorted([ l for l in df.legend.unique() if l.strip() and l not in ('-', 'ARSON','HOMICIDE') ])

    c = len(legends)
    ncols = 4.
    nrows = ceil(float(c)/ncols)

    cmap = plt.get_cmap('YlOrRd')

    fig, axes = plt.subplots(nrows=int(nrows), ncols=int(ncols), figsize=(10,10), 
                             squeeze=True, sharex=False, sharey=False)

    fig.set_size_inches(ncols*2.5,nrows*2.5)
    axes = axes.ravel() # Convert 2D array to 1D
    plt.tight_layout(h_pad=2)
    for i, legend in enumerate(legends):

        sub = df[df.legend == legend]
        
        if incident_type:
            sub = sub[sub.type == incident_type]
            
        axes[i].set_title(legend.title())
            
        if len(sub) < 40:
            continue
       
        heatg = sub.groupby(['dow','hour'])
        hgcounts = heatg.count()['id'].unstack('hour').fillna(0)
   
        # Converting to an array puts it into a for that
        # matplotlib expects. This probably only works b/c the
        # hours and days of week are 1-based indexes. 
        axes[i].pcolormesh(np.array(hgcounts.T),cmap=cmap)
        
from math import ceil
from IPython.display import display, clear_output

def plot_rhythm(df, legends = None, communities = None, incident_type=None, title=None, filename=None,
                axes_fields=['year','week'], ncols  = 2, scale = 1.0, height=2.5):
    """Just a more complex version of plot_heat_grid, which handles communities"""
    import numpy as np
    import matplotlib.pyplot as plt

    if not legends:
        legends = sorted([ l for l in df.legend.unique() if l.strip() and l not in ('-', 'ARSON','HOMICIDE') ])

    c = (len(legends) if legends else 1) * (len(communities) if communities else 1)
        
    if c == 0:
        c = 1
    
    if not communities:
        communities = [None]
    
    nrows = ceil(float(c)/ncols)

    cmap = plt.get_cmap('YlOrRd', 500)

    fig, axes = plt.subplots(nrows=int(nrows), ncols=int(ncols), figsize=(10,10), 
                             squeeze=True, sharex=False, sharey=False)

    axes = axes.ravel() # Convert 2D array to 1D

    fig.set_size_inches(12.0*scale,nrows*height*scale)
    
    plt.tight_layout(h_pad=2)
    fig.subplots_adjust(top=0.90)
    i = 0
    for community in communities:
        for legend in legends:

            
            sub = df
            gtitles = []
            
            if legend:
                sub = sub[sub.legend == legend]
                gtitles.append(legend.title())

            if community:
                sub = sub[sub.community == community]
                gtitles.append(community)
                
            if incident_type:
                sub = sub[sub.type == incident_type]

            clear_output(wait = True)
            print "Rendering ", i, ' of ', c
            axes[i].set_title(' / '.join(gtitles))

            if len(sub) < 40:
                i += 1
                continue

            heatg = sub.groupby(axes_fields)
            hgcounts = heatg.count()['id'].unstack(axes_fields[0]).fillna(0)

            # Converting to an array puts it into a for that
            # matplotlib expects. This probably only works b/c the
            # hours and days of week are 1-based indexes. 
            axes[i].pcolormesh(np.array(hgcounts.T),cmap=cmap)
            
            i += 1
            
        
    if title:
        fig.suptitle(title, fontsize=18, fontweight='bold')
        
    if filename:
        fig.savefig(filename)