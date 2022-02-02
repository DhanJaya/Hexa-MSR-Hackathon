from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd


def plot_data():
    summary_df = pd.read_csv('D:/hackathon/Summary/TotalSummary.csv')
    ccn = summary_df['CCN'].tolist()
    quality = summary_df['Quality'].tolist()
    vulns = summary_df['Num_Vulns'].tolist()

    # Creating figure
    fig = plt.figure(figsize=(16, 9))
    ax = plt.axes(projection="3d")

    # Creating plot
    ax.scatter3D(vulns, quality, ccn, color="green")
    plt.title("simple 3D scatter plot")
    ax.set_xlabel('vulns', fontweight='bold')
    ax.set_ylabel('quality', fontweight='bold')
    ax.set_zlabel('ccn', fontweight='bold')

    # show plot
    plt.show()

def plot_data1():
    summary_df = pd.read_csv('D:/hackathon/Summary/TotalSummary.csv')
    ccn = summary_df['CCN'].tolist()
    quality = summary_df['Quality'].tolist()
    vulns = summary_df['Num_Vulns'].tolist()

    positive_ccn = []
    positive_quality = []
    positive_vuln = []
    for ccn_val in ccn:
        positive_ccn.append(abs(ccn_val))
    for quality_val in quality:
        positive_quality.append(abs(quality_val))
    for vuln_val in vulns:
        positive_vuln.append(abs(vuln_val))


    # Creating figure
    # Creating figure
    fig = plt.figure(figsize=(16, 9))
    ax = plt.axes(projection="3d")

    # Add x, y gridlines
    ax.grid(b=True, color='grey',
            linestyle='-.', linewidth=0.3,
            alpha=0.2)

    # Creating color map
    my_cmap = plt.get_cmap('hsv')

    # Creating plot
    sctt = ax.scatter3D(ccn, quality, vulns,
                        alpha=0.8,
                        c=vulns,
                        cmap=my_cmap,
                        marker='^')
   # ax.view_init(-160, 70)
    plt.title("Quality analysis of PRs")
    ax.set_xlabel('CCN', fontweight='bold')
    ax.set_ylabel('Quality', fontweight='bold')
    ax.set_zlabel('Vulnerability', fontweight='bold')
    fig.colorbar(sctt, ax=ax, shrink=0.5, aspect=5)

    # show plot
    plt.show()

def retreieve_data_values():
    summary_df = pd.read_csv('D:/hackathon/Summary/TotalSummary.csv')
    ccn = summary_df['CCN'].tolist()
    quality = summary_df['Quality'].tolist()
    vulns = summary_df['Num_Vulns'].tolist()

    all_positive = 0
    two_positive = 0
    one_positve = 0
    non_positive = 0
    all_zero = 0
    for index in range(len(ccn)):
        ccn_positive = 0
        quality_positive = 0
        vuln_positive = 0
        if ccn[index] > 0:
            ccn_positive = 1
        if quality[index] > 0:
            quality_positive = 1
        if vulns[index] > 0:
            vuln_positive = 1
        total = ccn_positive + quality_positive + vuln_positive
        if total == 3:
            all_positive +=1
        elif total == 2:
            two_positive +=1
        elif total == 1:
            one_positve +=1
        elif ccn[index] ==0 and quality[index] ==0 and vulns[index] == 0:
            all_zero +=1
        else:
            non_positive +=1

    print('All positive = {}, two positive = {}, one positive = {} , all zero = {},  none positive = {}'.format(all_positive, two_positive, one_positve, all_zero, non_positive) )



#plot_data()

#plot_data1()

retreieve_data_values()


