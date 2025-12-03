#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <vector>
#include <algorithm>
 
#define MAXSIZE 1000001
 
using namespace std;
typedef pair<int, int> p;
typedef long long ll;

int n, m, k;
ll arr[MAXSIZE], segtree[MAXSIZE * 4], lazy[MAXSIZE * 4];

void create_segtree(int node, int start, int end) {
    if (start == end) {
        // if is leaf
        segtree[node] = arr[start];
        return;
    }

    int mid = (start + end) / 2;
    create_segtree(node * 2, start, end);
    create_segtree(node * 2 + 1, mid + 1, end);
    segtree[node] = segtree[node * 2] + segtree[node * 2 + 1];
}

void update_lazy(int node, int start, int end) {
    // reflect currnet node's lazy value
    if (lazy[node] != 0) {
        segtree[node]  += ((ll)end - start + 1) * lazy[node];
        if (start != end) {
            // if it is a section node,
            // the lazy value is passed on to both children

            lazy[node * 2] += lazy[node];
            lazy[node * 2 + 1] += lazy[node];
        }

        lazy[node] = 0;
    }
}


void update_range(int node, int start, int end, int l, int r, ll val) {
    update_lazy(node, start, end);

    if (l > end || r < start) return;

    if (l <= start && end <= r) {
        segtree[node] += ((ll)end - start + 1) * val;

        if (start != end) {
            lazy[node * 2] += val;
            lazy[node * 2 + 1] += val;
        }
        return;
    }

    int mid = (start + end) / 2;
    update_range(node * 2, start, mid, l, r, val);
    update_range(node * 2 + 1, mid + 1, end, l, r, val);
    segtree[node] = segtree[node * 2] + segtree[node * 2 + 1];
}


ll query(int node, int start, int end, int l, int r) {
    update_lazy(node, start, end);

    if (l > end || r < start) return 0;

    if (l >= start && end <= r) return segtree[node];

    int mid = (start + end) / 2;
    return query(node * 2, start, mid, l, r) + query(node * 2 + 1, mid + 1, end, l, r);
}

void init() {
    cin >> n >> m >> k;

    for (int i = 1; i <= n; i++){
        cin >> arr[i];
    } 
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(NULL);

    init();
    create_segtree(1, 1, n);

    int t, f, s, v;
    int udt = 0, qry = 0;

    while(1) {
        if (udt == m && qry == k) break;;
        cin >> t >> f >> s;
        if (t == 1) {
            cin >> v;
            update_range(1, 1, n, f, s, v);
            udt++;
        } else {
            printf("%lld\n", query(1, 1, n, f, s));
            qry++;
        }
    }

    return 0;
}