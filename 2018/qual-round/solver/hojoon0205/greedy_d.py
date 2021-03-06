inputfilename = input()
f = open("../../input/" + inputfilename + ".in", 'r')
lines = f.readlines()
#print(len(lines))

infos = lines[0].split()
for i in range(len(infos)):
    infos[i] = int(infos[i])

R = infos[0]
C = infos[1]
F = infos[2]
N = infos[3]
B = infos[4]
T = infos[5]

class Ride:
    def __init__(self, a, b, x, y, s, f, idx):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.s = s
        self.f = f
        self.idx = idx
        self.d = self.dist()
        self.e = self.lastOrder()
        assert(self.e >= self.s)

    def dist(self):
        return abs(self.x - self.a) + abs(self.y - self.b)

    def lastOrder(self):
        return self.f - self.dist()

class Taxi:
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t
        self.Rs = []

def dist(ax, ay, bx, by):
    return abs(ax-bx)+abs(ay-by)

rides = []
rides_idx = [0] * N

cnt = 0
for line in lines:
    cnt += 1
    if cnt == 1:
        continue
    l = line.split(' ')
    for i in range(len(l)):
        l[i] = int(l[i])
    
    rides.append( Ride(l[0], l[1], l[2], l[3], l[4], l[5], cnt-2) )

f.close()
#rides.sort(key=lambda r: r.e)
rides.sort(key=lambda r:(-r.d, r.e))

for i in range(N):
    rides_idx[rides[i].idx] = i

taxis = []
for i in range(F):
    taxis.append( Taxi(0, 0, 0) )

def available(newRs):
    tmp = Taxi(0, 0, 0)
    for ridx in newRs:
        ride = rides[rides_idx[ridx]]
        arrive_time = tmp.t + dist(ride.a, ride.b, tmp.x, tmp.y)
        if arrive_time > ride.e:
            return False
        if arrive_time >= ride.s:
            tmp.t = arrive_time + ride.d
        else:
            tmp.t = ride.s + ride.d
        tmp.x, tmp.y = ride.x, ride.y
    return True

def mov_dist(i, j, ride):
    if j == 0:
        beford = -1
    else:
        beford = taxis[i].Rs[j-1]
    
    if j == len(taxis[i].Rs):
        aftord = 99999
    else:
        aftord = taxis[i].Rs[j]

    if beford == -1:
        befdist = dist(0, 0, ride.a, ride.b)
    else:
        befride = rides[rides_idx[beford]]
        befdist = dist(befride.x, befride.y, ride.a, ride.b)
    
    if aftord == 99999:
        aftdist = 0
    else:
        aftride = rides[rides_idx[aftord]]
        aftdist = dist(ride.x, ride.y, aftride.a, aftride.b)
    
    return befdist+aftdist

cnt = 0
for ride in rides:
    cnt += 1
    idx_i = -1
    idx_j = -1
    for i in range(F):
        for j in range(len(taxis[i].Rs)+1):
            newRs = taxis[i].Rs[:j] + [ride.idx] + taxis[i].Rs[j:]
            if available(newRs):
                #idx_i = i
                #idx_j = j
                ########### fix later
                if idx_i < 0:
                    idx_i, idx_j = i, j
                else:
                    befmov = mov_dist(idx_i, idx_j, ride)
                    aftmov = mov_dist(i, j, ride)
                    if befmov > aftmov:
                        idx_i, idx_j = i, j
    
    if cnt%200 == 0:
        print(str(cnt)+"th ride finished")
        #print(idx_i, idx_j)

    if idx_i < 0:
        continue

    taxis[idx_i].Rs = taxis[idx_i].Rs[:idx_j] + [ride.idx] + taxis[idx_i].Rs[idx_j:]
    #print(taxis[idx_i].Rs)



f = open("./hojoon0205_dd2.out", "w")
for taxi in taxis:
    f.write(str(len(taxi.Rs)))
    for order in taxi.Rs:
        f.write(" " + str(order))
    f.write("\n")