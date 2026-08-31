"""Mini structural-form learner, after Kemp & Tenenbaum (2008)."""
import numpy as np
from scipy.cluster.hierarchy import linkage
from scipy.linalg import cho_factor, cho_solve

SIGMA = 1.0          # observation noise on each entity
WEIGHT = 3.0         # strength of every edge (fixed, and the same for every form)
THETA = np.exp(-3)   # complexity penalty per node, as in K&T

def _loglik(W, n_obs, D):
    """log P(D | S). W is the weighted adjacency over all nodes (observed first)."""
    m = W.shape[0]
    L = np.diag(W.sum(1)) - W
    P = L + np.eye(m) / SIGMA**2          # precision over all nodes
    Sig = np.linalg.inv(P)
    S = Sig[:n_obs, :n_obs]               # marginalise the latent nodes
    S = S + 1e-8*np.eye(n_obs)
    c = cho_factor(S)
    ld = 2*np.sum(np.log(np.diag(c[0])))
    ll = 0.0
    for k in range(D.shape[1]):
        f = D[:, k]
        ll += -0.5*(f @ cho_solve(c, f)) - 0.5*ld - 0.5*n_obs*np.log(2*np.pi)
    return ll

def _score(W, n_obs, D, groups=None):
    n_nodes = W.shape[0]
    return _loglik(W, n_obs, D) + n_nodes*np.log(THETA)

def _edges_to_W(n, edges, w=WEIGHT):
    W = np.zeros((n, n))
    for i, j in edges:
        W[i, j] = W[j, i] = w
    return W

# ---------- structure proposals, one per form ----------
def s_partition(D, kmax=6):
    from scipy.cluster.hierarchy import fcluster
    n = D.shape[0]; Zall = linkage(D, method='average'); best = None
    for k in range(1, min(kmax, n)+1):
        lab = np.zeros(n, int) if k == 1 else fcluster(Zall, k, criterion='maxclust') - 1
        # one latent hub per cluster
        W = np.zeros((n+k, n+k))
        for i in range(n):
            W[i, n+lab[i]] = W[n+lab[i], i] = WEIGHT
        sc = _score(W, n, D)
        if best is None or sc > best[0]: best = (sc, W, k)
    return best

def _order_score(order, D, closed):
    n = len(order)
    e = [(order[i], order[(i+1) % n]) for i in range(n if closed else n-1)]
    W = _edges_to_W(n, e)
    return _score(W, n, D), W

def _refine(order, D, closed, rounds=4):
    """2-opt: reverse a segment whenever it improves the score."""
    best, W = _order_score(order, D, closed)
    n = len(order)
    for _ in range(rounds):
        improved = False
        for i in range(n-1):
            for j in range(i+2, n):
                cand = np.concatenate([order[:i], order[i:j][::-1], order[j:]])
                sc, Wc = _order_score(cand, D, closed)
                if sc > best + 1e-9:
                    best, W, order, improved = sc, Wc, cand, True
        if not improved:
            break
    return best, W

def s_chain(D):
    order = np.argsort(_pc(D, 1)[:, 0])
    return _refine(order, D, closed=False)

def s_ring(D):
    p = _pc(D, 2)
    order = np.argsort(np.arctan2(p[:, 1], p[:, 0]))
    return _refine(order, D, closed=True)

def s_tree(D, kmax=8):
    """Cluster the entities, then build a hierarchy over the cluster hubs.
    Searching over the number of clusters keeps the tree from being charged
    for n-1 latent nodes it does not need."""
    from scipy.cluster.hierarchy import fcluster
    n = D.shape[0]; Zall = linkage(D, method='average'); best = None
    for k in range(2, min(kmax, n)+1):
        lab = fcluster(Zall, k, criterion='maxclust') - 1
        if len(np.unique(lab)) < k: continue
        cen = np.stack([D[lab == c].mean(0) for c in range(k)])
        Z = linkage(cen, method='average')
        m = n + k + (k-1)
        W = np.zeros((m, m))
        for i in range(n):                       # leaf -> its hub
            W[i, n+lab[i]] = W[n+lab[i], i] = WEIGHT
        for t, (a, b, _, _) in enumerate(Z):     # hubs joined into a hierarchy
            par = n + k + t
            W[int(a), par] = W[par, int(a)] = WEIGHT
            W[int(b), par] = W[par, int(b)] = WEIGHT
        sc = _score(W, n, D)
        if best is None or sc > best[0]: best = (sc, W, k)
    return best

def s_grid(D):
    n = D.shape[0]
    p = _pc(D, 2)
    side = int(np.ceil(np.sqrt(n)))
    # assign entities to lattice cells by sorting on the two components
    idx = np.lexsort((p[:, 1], p[:, 0]))
    pos = {}
    for r, i in enumerate(idx):
        pos[i] = (r // side, r % side)
    e = []
    inv = {v: k for k, v in pos.items()}
    for i in range(n):
        r, c = pos[i]
        for dr, dc in ((0, 1), (1, 0)):
            if (r+dr, c+dc) in inv: e.append((i, inv[(r+dr, c+dc)]))
    W = _edges_to_W(n, e)
    return _score(W, n, D), W

def _pc(D, k):
    X = D - D.mean(0)
    U, s, Vt = np.linalg.svd(X, full_matrices=False)
    return U[:, :k]*s[:k]

FORMS = {"partition": s_partition, "chain": s_chain, "ring": s_ring,
         "tree": s_tree, "grid": s_grid}

def discover_form(D, verbose=False):
    """Return (winning form, {form: log score}, extra info)."""
    D = np.asarray(D, float)
    D = D - D.mean(0)                     # centre each feature over the entities
    out, info = {}, {}
    for name, fn in FORMS.items():
        r = fn(D)
        out[name] = r[0]
        if len(r) > 2: info[name] = {"clusters": r[2]}
    best = max(out, key=out.get)
    if verbose:
        for k, v in sorted(out.items(), key=lambda z: -z[1]):
            extra = f"  (k={info[k]['clusters']})" if k in info else ""
            print(f"  {k:10s} {v:10.1f}{extra}{'   <-- best' if k == best else ''}")
    return best, out, info


# ---------- sampling data FROM a structure, to test recovery ----------
def sample_from(W, n_obs, n_feat, rng=None):
    """Draw n_feat features from N(0, (L_W + I/sigma^2)^{-1}), then keep the
    observed nodes. This is the generative model the scores assume."""
    rng = np.random.default_rng(rng)
    m = W.shape[0]
    L = np.diag(W.sum(1)) - W
    Sig = np.linalg.inv(L + np.eye(m)/SIGMA**2)
    X = rng.multivariate_normal(np.zeros(m), Sig, size=n_feat).T
    return X[:n_obs]

def W_ring(n):
    return _edges_to_W(n, [(i, (i+1) % n) for i in range(n)])

def W_chain(n):
    return _edges_to_W(n, [(i, i+1) for i in range(n-1)])

def W_partition(n, k):
    W = np.zeros((n+k, n+k))
    for i in range(n):
        c = i % k
        W[i, n+c] = W[n+c, i] = WEIGHT
    return W

def W_tree(n, k):
    """n leaves in k groups, the k hubs joined by a balanced binary hierarchy."""
    from scipy.cluster.hierarchy import linkage as _lk
    m = n + k + (k-1)
    W = np.zeros((m, m))
    for i in range(n):
        W[i, n + i % k] = W[n + i % k, i] = WEIGHT
    Z = _lk(np.arange(k).reshape(-1, 1), method='average')
    for t, (a, b, _, _) in enumerate(Z):
        par = n + k + t
        W[int(a), par] = W[par, int(a)] = WEIGHT
        W[int(b), par] = W[par, int(b)] = WEIGHT
    return W
