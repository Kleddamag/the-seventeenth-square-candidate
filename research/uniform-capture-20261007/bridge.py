#!/usr/bin/env python3
"""Independent rational root enclosure and coordinate bridge to H-261.

The contraction chain and upstream local theorem are separate dependencies.
"""
from fractions import Fraction as F
import argparse
import hashlib
import json
from pathlib import Path

import uniform as u

HERE=Path(__file__).resolve().parent
GRID=10**80
POLYNOMIALS=(
 ((0,1,1),(1,0,1),(1,1,-1),(1,2,-3),(2,0,-3),(2,2,1),(3,0,-1),(3,2,-1),(4,0,-1),(4,1,-1),(4,2,-1),(5,1,1)),
 ((0,1,-1),(0,2,4),(0,3,-1),(1,1,3),(1,2,-2),(1,3,-5),(1,4,2),(2,1,-4),(2,2,-2),(2,3,4),(2,4,2),(3,0,-2),(3,2,2),(4,0,-2),(4,1,1),(4,2,-2),(4,3,1),(5,1,1),(5,3,1)))


class I:
    def __init__(self,lo,hi=None):
        if isinstance(lo,I):
            self.lo,self.hi=lo.lo,lo.hi;return
        self.lo=F(lo);self.hi=F(lo if hi is None else hi)
        if self.lo>self.hi:
            raise ValueError('reversed interval')

    @classmethod
    def rounded(cls,lo,hi):
        return cls(F((lo*GRID).__floor__(),GRID),F((hi*GRID).__ceil__(),GRID))

    def __add__(self,other):
        other=I(other);return I.rounded(self.lo+other.lo,self.hi+other.hi)

    __radd__=__add__

    def __neg__(self):
        return I(-self.hi,-self.lo)

    def __sub__(self,other):
        return self+-I(other)

    def __rsub__(self,other):
        return I(other)+-self

    def __mul__(self,other):
        other=I(other);v=[x*y for x in (self.lo,self.hi) for y in (other.lo,other.hi)]
        return I.rounded(min(v),max(v))

    __rmul__=__mul__

    def __truediv__(self,other):
        other=I(other)
        if other.lo<=0<=other.hi:
            raise ValueError('division across zero')
        return self*I.rounded(1/other.hi,1/other.lo)

    def __rtruediv__(self,other):
        return I(other)/self

    def __pow__(self,n):
        if n<0:
            return 1/(self**(-n))
        result=I(1)
        for _ in range(n):
            result=result*self
        return result

    def absolute_upper(self):
        return max(abs(self.lo),abs(self.hi))

    def record(self):
        return [str(self.lo),str(self.hi)]


def evaluate(poly,x):
    return sum((F(c)*x[0]**a*x[1]**b for a,b,c in poly),F(0))


def derivative(poly,j):
    return tuple((a-int(j==0),b-int(j==1),c*(a if j==0 else b))
                 for a,b,c in poly if (a if j==0 else b)>0)


def root_enclosure():
    cert=json.loads((HERE/'upstream-root-certificate.json').read_text())
    declared=tuple(tuple((a,b,int(c)) for a,b,c in poly) for poly in cert['polynomials'])
    if declared!=POLYNOMIALS:
        raise ValueError('unexpected endpoint polynomials')
    midpoint=tuple(F(x) for x in cert['box']['midpoint'])
    raw=json.loads(u.p.SOURCE.read_text())
    if midpoint!=(F(raw['squares'][8]['t']),-F(raw['squares'][15]['t'])):
        raise ValueError('reference angles do not match the root midpoint')
    expected=[F(0)]*8+[midpoint[0]]*6+[F(0),-midpoint[1],F(0)]
    if [F(square['t']) for square in raw['squares']]!=expected:
        raise ValueError('reference orientation roster mismatch')
    radius=F(1,10**12)
    box=[I(x-radius,x+radius) for x in midpoint]
    jacobian=[[evaluate(derivative(poly,j),midpoint) for j in (0,1)] for poly in POLYNOMIALS]
    a,b=jacobian[0];c,d=jacobian[1];det=a*d-b*c
    if det==0:
        raise ValueError('singular midpoint Jacobian')
    inverse=((d/det,-b/det),(-c/det,a/det))
    jacobian_box=[[evaluate(derivative(poly,j),box) for j in (0,1)] for poly in POLYNOMIALS]
    matrix=[[I(int(i==j))-sum((inverse[i][k]*jacobian_box[k][j] for k in (0,1)),I(0))
             for j in (0,1)] for i in (0,1)]
    q=max(sum((x.absolute_upper() for x in row),F(0)) for row in matrix)
    f0=[evaluate(poly,midpoint) for poly in POLYNOMIALS]
    eta=max(abs(sum((inverse[i][k]*f0[k] for k in (0,1)),F(0))) for i in (0,1))
    if not q<1 or not eta+q*radius<radius:
        raise ValueError('contraction mapping criterion failed')
    tight=eta/(1-q)
    # Fixed outward grid avoids enormous intermediate rational denominators.
    tight_rounded=F((tight*10**55).__ceil__(),10**55)
    root=[I(x-tight_rounded,x+tight_rounded) for x in midpoint]
    return root,dict(method='Banach contraction for x -> x - J(midpoint)^-1 F(x)',
                     outer_radius=str(radius),derivative_norm_bound=str(q),
                     derivative_norm_decimal=float(q),midpoint_residual_bound=str(eta),
                     tight_root_radius=str(tight_rounded),
                     unique_root_in_outer_box=True,intervals=[x.record() for x in root])


def layout(t,beta):
    # H-254/H-256 formulae, re-expressed in this repository's label order.
    c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
    d=(1-beta*beta)/(1+beta*beta);e=2*beta/(1+beta*beta)
    side=(6+4*t)/(1+2*t-t*t)
    half=F(1,2);h=(c+s)/2
    x=half+(2+c*s+3*s-s*side)/c
    y=3*half+(2+3*c-c*side)/s
    aa=d*(x+half)-e*(side-1)+half
    bb=(d+e)*(side-1)-half
    u10=3*half+c*s+2*s;v10=c*(side-1)-s-half
    u11=c+2*s+half;v11=2*c+(c*c-s*s)/2-1
    u13=2*c+s+half;T=c*(c+4-side)
    rot=lambda a,b:(c*a-s*b,s*a+c*b)
    points=[(half,half),(side-half,half),(3*half,half),
            (side-3*half-T/(3*s),half),(half,3*half),(side-half,3*half),
            (half,side-half),(side-half,side-half),(h,2+h),rot(u10,v10),rot(u11,v11),
            rot(u11+1,v10-1),rot(u13,v11-1-T/3),rot(u13+1,v10-2),
            (x,side-half),(d*aa+e*bb,-e*aa+d*bb),(side-half,y)]
    return side,points,(c,s),(-s,c)


def run(cert_path):
    root,root_receipt=root_enclosure()
    side_star,points_star,u_star,v_star=layout(*root)
    side,points,axes,corners,H,G=u.geometry()
    if side_star.hi>side:
        raise ValueError('rational cap not above algebraic side')
    cert=json.loads(cert_path.read_text())
    if cert['source_sha256']!=hashlib.sha256(u.p.SOURCE.read_bytes()).hexdigest():
        raise ValueError('source digest mismatch')
    # Square 8's x reach is at least 1/2 at every orientation. Its input
    # position interval alone implies the contractor's lower side bound.
    side_floor=points[7][0]+F(1,2)-F(cert['radius'])
    if side_floor<side-F(1,50):
        raise ValueError('input neighbourhood does not imply the side floor')
    bounds=[tuple(map(F,pair)) for pair in cert['final_bounds']]
    drift=[]
    for i in range(17):
        if i==3:
            continue
        if i in (10,12):
            difference=[I(points[i][k])-points_star[i][k] for k in (0,1)]
            offset=sum((u_star[k]*difference[k] for k in (0,1)),I(0)).absolute_upper()
            cross=sum((u_star[k]*axes[i][1][k] for k in (0,1)),I(0)).absolute_upper()
            parameter=21 if i==10 else 25
            extra=offset+max(abs(x) for x in bounds[parameter])*cross
            drift.append((2*i,extra))
        else:
            for k in (0,1):
                index=2*i+k
                if index in u.CORE:
                    drift.append((index,(I(points[i][k])-points_star[i][k]).absolute_upper()))
    angle_drift=2*F(root_receipt['tight_root_radius'])
    for index in u.ANGLES:
        drift.append((index,angle_drift if index-34 in range(8,14) or index-34==15 else F(0)))
    if {i for i,_ in drift}!=set(u.CORE):
        raise ValueError('incomplete coordinate bridge')
    transferred={str(i):str(max(abs(x) for x in bounds[i])+error) for i,error in drift}
    largest=max(F(x) for x in transferred.values())
    if largest>=F(1,5000):
        raise ValueError('output does not enter the upstream local radius')
    # Exact-root slides, with a>=0 supplied directly by the physical right wall
    # and S<=S*. Do not assume that a boundary rational slide stays in B'_W.
    a_root=I(*bounds[2])+side_star-F(1,2)-points[1][0]
    parameter_bounds={'a':[str(max(F(0),a_root.lo)),str(a_root.hi)]}
    for i,parameter,sign,name in ((10,21,-1,'b'),(12,25,1,'z')):
        difference=[I(points[i][k])-points_star[i][k] for k in (0,1)]
        offset=sum((v_star[k]*difference[k] for k in (0,1)),I(0))
        cross=sum((v_star[k]*axes[i][0][k] for k in (0,1)),I(0))
        along=sum((v_star[k]*axes[i][1][k] for k in (0,1)),I(0))
        projected=sign*offset+sign*cross*I(*bounds[2*i])+along*I(*bounds[parameter])
        parameter_bounds[name]=projected.record()
    pad=F(1,10**12)
    padded={'a':(F(0),F(1,4)+pad),'b':(-F(1,2500)-pad,F(1,12)+pad),'z':(-F(1,8)-pad,F(1,16)+pad)}
    for name,pair in parameter_bounds.items():
        lo,hi=map(F,pair)
        if not padded[name][0]<=lo<=hi<=padded[name][1]:
            raise ValueError('exact-root slides outside the padded rigidity box')
    receipt=dict(status='PASS',root=root_receipt,
                 contraction_certificate_sha256=hashlib.sha256(cert_path.read_bytes()).hexdigest(),
                 upstream_root_certificate_sha256=hashlib.sha256((HERE/'upstream-root-certificate.json').read_bytes()).hexdigest(),
                 exact_side_interval=side_star.record(),rational_cap=str(side),
                 side_floor_from_square_8=str(side_floor),
                 maximum_coordinate_reference_drift=str(max(error for _,error in drift)),
                 transferred_core_bounds=transferred,maximum_transferred_radius=str(largest),
                 transferred_parameters=parameter_bounds,
                 padded_parameter_box={name:[str(lo),str(hi)] for name,(lo,hi) in padded.items()},
                 physical_side_hypothesis='S <= S*; used for a_exact >= 0',
                 maximum_transferred_radius_decimal=float(largest),target_radius='1/5000',
                 dependencies=['Separately replay the contraction certificate matching its digest.',
                               'Replay uniform-rigidity.json to obtain exact equality on the padded box without an occupancy premise.',
                               'Physical containment of square 8 supplies the input side floor.'],
                 conclusion='Coordinate inclusion proved; no claim that arbitrary packings enter the input tube.')
    return receipt


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate',type=Path,nargs='?',default=HERE/'uniform-full-box.json')
    parser.add_argument('--output',type=Path,default=HERE/'bridge-receipt.json')
    args=parser.parse_args()
    receipt=run(args.certificate)
    args.output.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ('status','maximum_coordinate_reference_drift','maximum_transferred_radius_decimal','target_radius')},indent=2))


if __name__=='__main__':
    main()
