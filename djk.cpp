#include<iostream>
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<queue>
#include<cmath>
using namespace std;
char buff[500];
char templine[500];
const int SIZE=100010;
int head[SIZE],n,m,s,ecnt;
double dis[SIZE];
bool vis[SIZE];
bool gen[SIZE];
struct node
{
    node(int _id, double _w):id(_id), w(_w){}
    int id;
    double w;
};
struct edge
{
    edge(int _v, int _nxt, double _dist):v(_v),nxt(_nxt),dist(_dist){}
    edge(){}
    int v,nxt;
    double dist;
}e[SIZE];
bool operator <(node a,node b)
{
    return (a.w>b.w);
}
void add_edge(int from,int to,double dis)
{
    e[++ecnt]=edge(to,head[from],dis);
    head[from]=ecnt;
}

void dijkstra(int u, int maxid)
{
    for (int i = 0; i <= maxid; ++i) {
        dis[i] = 999999999;
    }
    memset(vis,0,sizeof(vis));
    priority_queue<node> q;
    dis[u]=0;
    q.push(node(u,0));
    while(!q.empty())
    {
        //printf("qn");
        node flag=q.top();
        q.pop();
        int v=flag.id;
        if(vis[v]) continue;
        vis[v]=1;
        for(int i=head[v];i;i=e[i].nxt)
        {
            int to=e[i].v;
            if(dis[to]>dis[v]+e[i].dist)
            {
                dis[to]=dis[v]+e[i].dist;
                q.push(node(to,dis[to]));
            }
        }
    }
    //printf("%dout", u);
}
int trans[SIZE];
int readEdge() {
    memset(trans, 0, sizeof(trans));
    int maxid = 0;
    freopen("LF.L1", "r", stdin);
    while (gets(templine)) {
        ++maxid;
    }
    freopen("LF.L2", "r", stdin);
    int id, mark, left, right;
    double R, X;
    while (gets(templine)) {
        sscanf(templine, "%d,%d,%d,%d,%lf,%lf,%s", &mark, &left, &right, &id, &R, &X, buff);
        // printf("%d %d %d %d %f %f\n", mark, left, right, id, R, X);
        if (mark == 1) {
            double dis = sqrt(R * R + X * X);
            add_edge(left, right, dis);
            add_edge(right, left, dis);
            if (left > maxid) maxid = left;
            if (right > maxid) maxid = right;
        }
    }
    freopen("LF.L3", "r", stdin);
    while (gets(templine)) {
        sscanf(templine, "%d,%d,%d,%s", &mark, &left, &right, buff);
        if (mark == 1) {
            if (left > 0) {
                add_edge(left, right, 0);
                add_edge(right, left, 0);
            }
            else {
                if (trans[-left] == 0) {
                    trans[-left] = ++maxid;
                }
                add_edge(trans[-left], right, 0);
                add_edge(right, trans[-left], 0);
            }
        }
    }
    return maxid;
}

int readGen() {
    freopen("LF.L5", "r", stdin);
    int mark, id, cnt = 0;
    while (gets(templine)) {
        sscanf(templine, "%d,%d,%s", &mark, &id, buff);
        if (mark == 1) {
            gen[id] = 1;
            ++cnt;
        }
    }
    return cnt;
}

struct disnode {
    disnode(int _genid, double _dis):genid(_genid), dis(_dis){}
    int genid;
    double dis;
};

struct bus {
    disnode* list;
    int cnt;
    void add_gen(int genid, double dis) {
        list[cnt] = disnode(genid, dis);
        ++cnt;
    }
};

bus* buslist;

bool cmp(disnode a, disnode b) {
    return a.dis < b.dis;
}

char busname[SIZE][30];
void getname(){
    char c;
    // stroe the busname
    freopen("LF.L1", "r", stdin);
    int ignore = 2;
    int linenum = 0;
    int id = 0;
    while (scanf("%c", &c) != EOF) {
        if (ignore == 1) {
            if (c == '\r' || c == '\n') {
                ignore = 2;
                continue;
            }
        }
        if (ignore == 2) {
            if (c == '\'') {
                ++linenum;
                id = 0;
                ignore = 0;
                continue;
            }
        }
        if (ignore == 0) {
            if (c == '\'') {
                busname[linenum][id++] = '\0';
                ignore = 1;
                continue;
            }
            busname[linenum][id++] = c;
        }
    }
}

int main() {
    getname();
    int busnum = readEdge();
    int gennum = readGen();
    printf("%d %d\n", busnum, gennum);
    buslist = (bus*)malloc(sizeof(bus) * (busnum+60));
    for (int i = 0; i <= busnum; ++i) {
        buslist[i].list = (disnode*)malloc(sizeof(disnode) * (gennum+60));
        buslist[i].cnt = 0;
    }
    for (int i = 0; i <= busnum; ++i) {
        if (gen[i]) {
            printf("\r%d/%d", i, busnum);
            dijkstra(i, busnum);
            for (int j = 1; j <= busnum; ++j) {
                buslist[j].add_gen(i, dis[j]);
            }
        }
    }
    printf("\r----end-----\n");
    for (int i = 1; i <= busnum; ++i) {
        sort(buslist[i].list, buslist[i].list + gennum, cmp);
    }
    freopen("out.dis", "w", stdout);
    for (int i = 1; i <= busnum; ++i) {
        for (int j = 0; j < gennum; ++j) {
            printf("%d:%f, ", buslist[i].list[j].genid, buslist[i].list[j].dis);
        }
        printf("\n");
    }
    freopen("nameout.dis", "w", stdout);
    for (int i = 1; i <= busnum; ++i) {
        printf("%s:", busname[i]);
        for (int j = 0; j < gennum; ++j) {
            printf("%s, ", busname[buslist[i].list[j].genid]);
        }
        printf("\n");
    }
    return 0;
}