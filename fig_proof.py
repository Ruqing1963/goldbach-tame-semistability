"""
fig_proof.py — Figures for Paper #13
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

magma_data = [
    (3,  7,   {2:8, 3:2, 5:2, 7:2}),
    (7,  23,  {2:4, 3:2, 5:2, 7:2, 23:2}),
    (11, 19,  {2:7, 3:2, 5:2, 11:2, 19:2}),
    (13, 17,  {2:8, 3:2, 5:2, 13:2, 17:2}),
    (3,  17,  {2:8, 3:2, 5:2, 7:2, 17:2}),
    (7,  19,  {2:8, 3:2, 7:2, 13:2, 19:2}),
    (3,  37,  {2:7, 3:2, 5:2, 17:2, 37:2}),
    (7,  41,  {2:4, 3:2, 7:2, 17:2, 41:2}),
    (7,  53,  {2:8, 3:2, 5:2, 7:2, 23:2, 53:2}),
    (11, 37,  {2:4, 3:2, 11:2, 13:2, 37:2}),
]

# ═══════════════════════════════════════════════════════════════
# FIGURE 1: Classification of all 40 odd primes into 4 cases
# ═══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5.5))

case_colors = {'I': '#2255BB', 'II': '#CC3333', 'III': '#228833', 'IV': '#CC8822'}
case_markers = {'I': 'o', 'II': 's', 'III': '^', 'IV': 'D'}

points = {'I': [], 'II': [], 'III': [], 'IV': []}

for idx, (p, q, fac) in enumerate(magma_data):
    N = (p + q) // 2
    diff = abs(p - q)
    for r in sorted(r for r in fac if r > 2):
        if r == p:
            case = 'I'
        elif r == q:
            case = 'II'
        elif N % r == 0:
            case = 'III'
        elif diff % r == 0:
            case = 'IV'
        points[case].append((idx, r))

for case, pts in points.items():
    if pts:
        xs, ys = zip(*pts)
        ax.scatter(xs, ys, c=case_colors[case], marker=case_markers[case],
                  s=70, edgecolors='black', linewidths=0.5, zorder=5,
                  label=f'Case {case}')

# Labels
case_labels = [f"({p},{q})" for p, q, _ in magma_data]
ax.set_xticks(range(len(case_labels)))
ax.set_xticklabels(case_labels, rotation=45, fontsize=8, ha='right')
ax.set_ylabel(r'Bad odd prime $r$', fontsize=12)
ax.set_title('Classification of 40 bad odd primes into four cases', fontsize=12)

legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#2255BB',
           markersize=9, markeredgecolor='k', label=r'Case I: $r = p$ (cusp)'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='#CC3333',
           markersize=9, markeredgecolor='k', label=r'Case II: $r = q$ (cusp)'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='#228833',
           markersize=9, markeredgecolor='k', label=r'Case III: $r \mid N$ (2 nodes)'),
    Line2D([0], [0], marker='D', color='w', markerfacecolor='#CC8822',
           markersize=9, markeredgecolor='k', label=r'Case IV: $r \mid (p{-}q)$ (2 nodes)'),
]
ax.legend(handles=legend_elements, fontsize=9, loc='upper left')
ax.set_yscale('log')
ax.grid(True, alpha=0.15)
plt.tight_layout()
plt.savefig('/home/claude/paper13/figures/fig_classification.pdf', dpi=300, bbox_inches='tight')
plt.savefig('/home/claude/paper13/figures/fig_classification.png', dpi=200, bbox_inches='tight')
plt.close()
print("Figure 1 done.")


# ═══════════════════════════════════════════════════════════════
# FIGURE 2: The proof diagram — two paths to 2a + t = 2
# ═══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Panel (a): Cusp case — Cases I, II
ax = axes[0]
ax.set_xlim(-0.5, 5.5)
ax.set_ylim(-0.5, 4.5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title(r'(a) Cases I \& II: $r = p$ or $r = q$', fontsize=12, fontweight='bold')

# Draw root collision diagram
roots_x = [1, 2, 3, 4, 5]
roots_labels = ['0', r'$p$', r'$-p$', r'$q$', r'$-q$']
for i, (rx, rl) in enumerate(zip(roots_x, roots_labels)):
    color = '#CC3333' if i < 3 else '#2255BB'
    ax.plot(rx, 3.8, 'o', color=color, markersize=12, markeredgecolor='k', zorder=5)
    ax.text(rx, 4.15, rl, ha='center', fontsize=10)

# Collision bracket for {0, p, -p}
ax.annotate('', xy=(0.7, 3.5), xytext=(3.3, 3.5),
           arrowprops=dict(arrowstyle='-', lw=1.5, color='#CC3333'))
ax.text(2, 3.2, 'collide mod $r$', ha='center', fontsize=8, color='#CC3333')

# Arrow to reduced curve
ax.annotate('', xy=(3, 2.5), xytext=(3, 2.9),
           arrowprops=dict(arrowstyle='->', lw=1.5, color='gray'))

# Reduced curve box
bbox1 = FancyBboxPatch((0.3, 1.6), 5, 0.8, boxstyle="round,pad=0.1",
                        facecolor='#FFEEEE', edgecolor='#CC3333', linewidth=1.5)
ax.add_patch(bbox1)
ax.text(2.8, 2.0, r'$\bar{C}: y^2 = x^3(x^2 - \bar{q}^2)$    [1 cusp at origin]',
       ha='center', fontsize=10)

# Arrow to Néron data
ax.annotate('', xy=(3, 0.9), xytext=(3, 1.5),
           arrowprops=dict(arrowstyle='->', lw=1.5, color='gray'))

# Result box
bbox2 = FancyBboxPatch((0.3, 0.0), 5, 0.8, boxstyle="round,pad=0.1",
                        facecolor='#EEEEFF', edgecolor='#2255BB', linewidth=1.5)
ax.add_patch(bbox2)
ax.text(2.8, 0.4, r'$(a,t,u) = (1,0,1)$   $\Rightarrow$   $2a+t = 2$   $\Rightarrow$   $f_r = 2$',
       ha='center', fontsize=11, fontweight='bold')

# Panel (b): Node case — Cases III, IV
ax = axes[1]
ax.set_xlim(-0.5, 5.5)
ax.set_ylim(-0.5, 4.5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title(r'(b) Cases III \& IV: $r \mid N$ or $r \mid (p{-}q)$', fontsize=12, fontweight='bold')

# Draw root collision diagram
for i, (rx, rl) in enumerate(zip(roots_x, roots_labels)):
    if i == 0:
        color = '#228833'
    elif i in [1, 3]:
        color = '#CC8822'
    else:
        color = '#CC8822'
    ax.plot(rx, 3.8, 'o', color=color, markersize=12, markeredgecolor='k', zorder=5)
    ax.text(rx, 4.15, rl, ha='center', fontsize=10)

# Collision brackets for {p, q} and {-p, -q}
ax.annotate('', xy=(1.7, 3.5), xytext=(4.3, 3.5),
           arrowprops=dict(arrowstyle='-', lw=1.5, color='#CC8822'))
ax.text(3, 3.2, r'$p \equiv \pm q$ mod $r$', ha='center', fontsize=8, color='#CC8822')

# Arrow
ax.annotate('', xy=(3, 2.5), xytext=(3, 2.9),
           arrowprops=dict(arrowstyle='->', lw=1.5, color='gray'))

# Reduced curve box
bbox3 = FancyBboxPatch((0.1, 1.6), 5.2, 0.8, boxstyle="round,pad=0.1",
                        facecolor='#EEFFEE', edgecolor='#228833', linewidth=1.5)
ax.add_patch(bbox3)
ax.text(2.7, 2.0, r'$\bar{C}: y^2 = x(x-\bar{a})^2(x+\bar{a})^2$    [2 nodes]',
       ha='center', fontsize=10)

# Arrow
ax.annotate('', xy=(3, 0.9), xytext=(3, 1.5),
           arrowprops=dict(arrowstyle='->', lw=1.5, color='gray'))

# Result box
bbox4 = FancyBboxPatch((0.1, 0.0), 5.2, 0.8, boxstyle="round,pad=0.1",
                        facecolor='#EEEEFF', edgecolor='#2255BB', linewidth=1.5)
ax.add_patch(bbox4)
ax.text(2.7, 0.4, r'$(a,t,u) = (0,2,0)$   $\Rightarrow$   $2a+t = 2$   $\Rightarrow$   $f_r = 2$',
       ha='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('/home/claude/paper13/figures/fig_proof_diagram.pdf', dpi=300, bbox_inches='tight')
plt.savefig('/home/claude/paper13/figures/fig_proof_diagram.png', dpi=200, bbox_inches='tight')
plt.close()
print("Figure 2 done.")
