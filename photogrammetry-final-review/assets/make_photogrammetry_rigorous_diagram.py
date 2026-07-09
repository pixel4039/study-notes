from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
W,H=1800,1150
img=Image.new('RGB',(W,H),'white')
d=ImageDraw.Draw(img)

def ft(size,bold=False):
    paths=['/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc','/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    for p in paths:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()
Ftitle=ft(42,True); Fh=ft(31,True); F=ft(25); Fs=ft(21); Fm=ft(27,True); Fsmall=ft(18)
blue=(20,96,190); red=(210,40,35); green=(30,130,70); gray=(90,90,90); light=(248,250,252)

def text(x,y,s,font=F,fill=(0,0,0),anchor=None): d.text((x,y),s,font=font,fill=fill,anchor=anchor)
def line(p,fill=(0,0,0),w=3): d.line(p,fill=fill,width=w)
def dot(x,y,r=7,fill=(0,0,0),outline=None):
    d.ellipse((x-r,y-r,x+r,y+r),fill=fill,outline=outline,width=2 if outline else 1)
def arrow(p1,p2,fill=red,w=4):
    d.line((*p1,*p2),fill=fill,width=w)
    ang=math.atan2(p2[1]-p1[1],p2[0]-p1[0]); L=18
    pts=[p2,(p2[0]-L*math.cos(ang-0.38),p2[1]-L*math.sin(ang-0.38)),(p2[0]-L*math.cos(ang+0.38),p2[1]-L*math.sin(ang+0.38))]
    d.polygon(pts,fill=fill)
def dashed(p1,p2,fill=gray,w=2,seg=14):
    x1,y1=p1; x2,y2=p2; L=math.hypot(x2-x1,y2-y1); n=max(1,int(L/seg))
    for i in range(0,n,2):
        a=i/n; b=min((i+1)/n,1)
        d.line((x1+(x2-x1)*a,y1+(y2-y1)*a,x1+(x2-x1)*b,y1+(y2-y1)*b),fill=fill,width=w)

def project_point_to_line(S,P,line_y):
    # intersection of S->P with horizontal y=line_y
    sx,sy=S; px,py=P
    t=(line_y-sy)/(py-sy)
    return (sx+t*(px-sx), line_y)

text(W/2,28,'考试严谨版：像片倾斜位移 与 地形起伏位移',Ftitle,anchor='ma')
text(W/2,80,'重点不是画复杂，而是标清：理想位置 vs 实际位置、辐射中心、位移方向',F,gray,anchor='ma')
# panels
for box in [(45,125,875,910),(925,125,1755,910)]:
    d.rounded_rectangle(box,radius=22,fill=light,outline=(25,25,25),width=3)

# LEFT: tilt displacement - abstract rigorous exam schematic
text(460,155,'① 像片倾斜引起的像点位移',Fh,anchor='ma')
text(460,198,'比较：水平像片上的理论像点 a₀  →  倾斜像片上的实际像点 a',F,anchor='ma')
# planes
# horizontal reference image plane
line((140,560,790,560),gray,3); text(640,530,'水平像片面（参考）',Fs,gray)
# tilted image plane
x1,y1=145,690; x2,y2=795,430
line((x1,y1,x2,y2),(0,0,0),4); text(155,710,'倾斜像片面',Fs)
# camera center
S=(465,300); dot(*S,8); text(S[0]+18,S[1]-32,'S 摄影中心',Fm)
# vertical principal axis and plumb line indicators
# define special points on tilted plane roughly collinear along max slope: n,o,c,i
# Line y = y1 + slope(x-x1)
slope=(y2-y1)/(x2-x1)
def y_on_tilt(x): return y1+slope*(x-x1)
# place points distinct along tilted plane
n=(360,y_on_tilt(360)); o=(430,y_on_tilt(430)); c=(505,y_on_tilt(505)); i=(575,y_on_tilt(575))
# dashed vertical plumb through S to n (schematic)
dashed(S,n,blue,2); text(n[0]-95,n[1]-20,'n 像底点',Fs,blue)
dot(*n,7,blue)
# principal point o on tilted plane
line((S[0],S[1],o[0],o[1]),fill=gray,w=2); dot(*o,7,green); text(o[0]-58,o[1]+16,'o 像主点',Fs,green)
# isocenter c
# equal scale point i optional
for pt,label,col,dy in [(c,'c 等角点',red,-42),(i,'i 等比点',gray,20)]:
    dot(*pt,7,col); text(pt[0]+10,pt[1]+dy,label,Fs,col)
# object rays and points
# choose actual image point a on tilted plane, theoretical a0 on horizontal ref along same object ray schematic
Atilt=(665,y_on_tilt(665)); A0=(610,560)
line((S[0],S[1],Atilt[0],Atilt[1]),(80,80,80),2)
dot(*A0,6,(0,0,0)); text(A0[0]-58,A0[1]+14,'a₀ 理论像点',Fs)
dot(*Atilt,7,red); text(Atilt[0]+12,Atilt[1]-26,'a 实际像点',Fs,red)
arrow(A0,Atilt,red,4); text((A0[0]+Atilt[0])/2+20,(A0[1]+Atilt[1])/2,'δₜ 倾斜位移',Fm,red)
# radial lines from c
line((c[0],c[1],Atilt[0],Atilt[1]),blue,2); dashed(c,A0,blue,2)
text(205,805,'结论：倾斜位移具有辐射性，辐射中心为等角点 c',Fm,red)
text(205,846,'记忆：相机姿态歪了 → 看 c；不要和像底点 n 混淆。',F)

# RIGHT: relief displacement rigorous central projection schematic
text(1340,155,'② 地形起伏引起的像点位移（投影差）',Fh,anchor='ma')
text(1340,198,'比较：基准面点 A₀ 的像 a₀  →  实际高程点 A 的像 a',F,anchor='ma')
# image plane
img_y=385
line((1030,img_y,1650,img_y),(0,0,0),4); text(1515,img_y-35,'像片面',Fs)
# S and nadir
S2=(1340,260); dot(*S2,8); text(S2[0]+18,S2[1]-30,'S 摄影中心',Fm)
n2=(1340,img_y); dot(*n2,8,blue); text(n2[0]+10,n2[1]+15,'n 像底点',Fm,blue)
dashed(S2,n2,blue,2)
# terrain/reference plane
base_y=775
line((1010,base_y,1680,base_y),gray,3); text(1545,base_y+18,'基准面 / 平均高程面',Fs,gray)
# terrain bump
terrain=[(1010,770),(1110,760),(1200,735),(1280,695),(1340,660),(1395,625),(1450,655),(1510,710),(1600,755),(1680,770)]
d.line(terrain,fill=(0,0,0),width=4,joint='curve')
# actual ground point A and base A0 choose off nadir to show radial displacement
A=(1460,650); A0=(1460,base_y)
dot(*A,8,red); text(A[0]+16,A[1]-30,'A 实际高程点',Fm,red)
dot(*A0,7); text(A0[0]+16,A0[1]+8,'A₀ 基准面对应点',Fs)
dashed(A,A0,red,3); text(A[0]+28,(A[1]+A0[1])/2,'h',Fm,red)
# projections to image plane
a=project_point_to_line(S2,A,img_y); a0=project_point_to_line(S2,A0,img_y)
line((S2[0],S2[1],A[0],A[1]),(80,80,80),2)
line((S2[0],S2[1],A0[0],A0[1]),(80,80,80),2)
dot(a0[0],a0[1],7); text(a0[0]-55,a0[1]-42,'a₀',Fs)
dot(a[0],a[1],8,red); text(a[0]+8,a[1]-42,'a',Fs,red)
arrow(a0,a,red,4); text((a0[0]+a[0])/2-15,img_y-82,'δh',Fm,red)
# radial distance r from n to a0/a
dashed(n2,a0,blue,2); dashed(n2,a,blue,2)
text((n2[0]+a0[0])/2,img_y+18,'r',Fm,blue)
# direction note
arrow((n2[0]+25,n2[1]+45),(a[0]-5,a[1]+45),blue,3)
text(1115,455,'位移沿 n → 像点 的径向方向',Fs,blue)
# formula box
text(1045,805,'结论：地形起伏位移/投影差以像底点 n 为辐射中心',Fm,red)
text(1045,846,'近似关系：δh ≈ r · h / H',Fm)
text(1045,883,'所以：离 n 越远 r 越大、地面高差 h 越大，位移越大；航高 H 越大，位移越小。',Fs)

# bottom exam answer box
d.rounded_rectangle((100,955,1700,1110),radius=24,fill=(238,246,255),outline=blue,width=4)
text(900,980,'考试答案框',Fh,blue,anchor='ma')
text(140,1028,'像片倾斜位移：由像片平面倾斜引起，比较水平像片理论位置与倾斜像片实际位置；位移呈辐射状，辐射中心为等角点 c。',F)
text(140,1070,'地形起伏位移：由地面点相对基准面的高差 h 引起，又称投影差；位移沿像底点 n 到像点的径向方向，辐射中心为像底点 n。',F)
text(900,1120,'口诀：倾斜找 c，起伏找 n',Fh,red,anchor='ma')

out='/home/ubuntu/resources/photogrammetry_displacement_exam_rigorous.png'
img.save(out)
print(out)
print(Path(out).stat().st_size)
