from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
W,H=1400,900
img=Image.new('RGB',(W,H),'white')
d=ImageDraw.Draw(img)

def font(size,bold=False):
    candidates=[
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    ]
    for p in candidates:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()
Ftitle=font(34,True); Fsub=font(25,True); F=font(21); Fs=font(18); Fm=font(22,True)

def text(x,y,s,f=F,fill=(0,0,0),anchor=None): d.text((x,y),s,font=f,fill=fill,anchor=anchor)
def line(points,fill=(0,0,0),w=3): d.line(points,fill=fill,width=w)
def dash(p1,p2,fill=(120,120,120),w=2,step=14):
    import math
    x1,y1=p1; x2,y2=p2; L=math.hypot(x2-x1,y2-y1); n=int(L/step)
    for i in range(0,n,2):
        a=i/n; b=min((i+1)/n,1); d.line((x1+(x2-x1)*a,y1+(y2-y1)*a,x1+(x2-x1)*b,y1+(y2-y1)*b),fill=fill,width=w)
def arrow(p1,p2,fill=(210,30,30),w=4):
    d.line((*p1,*p2),fill=fill,width=w)
    import math
    ang=math.atan2(p2[1]-p1[1],p2[0]-p1[0]); L=14
    pts=[p2,(p2[0]-L*math.cos(ang-0.35),p2[1]-L*math.sin(ang-0.35)),(p2[0]-L*math.cos(ang+0.35),p2[1]-L*math.sin(ang+0.35))]
    d.polygon(pts,fill=fill)
def dot(x,y,r=6,fill=(0,0,0)): d.ellipse((x-r,y-r,x+r,y+r),fill=fill)

text(700,25,'摄影测量：像片倾斜位移 vs 地形起伏位移',Ftitle,anchor='ma')
d.rounded_rectangle((45,90,675,725),radius=18,outline=(30,30,30),width=2,fill=(251,251,251))
d.rounded_rectangle((725,90,1355,725),radius=18,outline=(30,30,30),width=2,fill=(251,251,251))

# left
text(360,112,'① 像片倾斜引起的像点位移',Fsub,anchor='ma')
text(360,150,'相机没有垂直向下拍，像平面“歪了”',F,anchor='ma')
dot(360,245,7); text(375,226,'S 摄影中心',Fm)
dash((170,490),(550,490)); text(555,481,'水平像平面参考',Fs)
line((160,545,565,425),w=3); text(170,555,'倾斜像平面',Fs)
for p in [(210,530),(470,453),(540,433)]: line((360,245,*p),fill=(80,80,80),w=2)
dot(355,487,8,(18,102,204)); text(368,500,'c 等角点',Fm,(18,102,204))
for a,b in [((260,515),(224,526)),((455,457),(493,446)),((395,475),(414,469))]:
    dot(*a,6); dot(*b,6,(210,30,30)); arrow(a,b)
d.rounded_rectangle((90,610,620,698),radius=14,outline=(212,164,0),width=2,fill=(255,247,214))
text(112,628,'辐射中心：等角点 c',Fm)
text(112,660,'记法：相机“倾斜”了 → 找 c',F)

# right
text(1040,112,'② 地形起伏引起的像点位移',Fsub,anchor='ma')
text(1040,150,'地面有高差，高处离相机近，投影位置变了',F,anchor='ma')
dot(1040,235,7); text(1055,216,'S 摄影中心',Fm)
line((840,365,1240,365),w=3); text(1245,352,'像平面',Fs)
dot(1040,365,8,(18,102,204)); text(1053,382,'n 像底点',Fm,(18,102,204))
# terrain curve approximate as polyline
terrain=[(820,640),(900,620),(970,590),(1018,550),(1048,520),(1085,485),(1115,570),(1160,585),(1210,603),(1290,635)]
d.line(terrain,fill=(0,0,0),width=3,joint='curve')
dash((820,640),(1290,640)); text(1260,650,'基准面',Fs)
dot(1048,520,7,(210,30,30)); text(1060,498,'A 山顶',Fm)
dot(1048,640,6); text(1060,648,'A₀ 平地点',Fm)
dash((1048,520),(1048,640),fill=(210,30,30),w=3); text(1016,570,'h',Fm,(210,30,30))
line((1040,235,1048,520),fill=(80,80,80),w=2); line((1040,235,1048,640),fill=(80,80,80),w=2)
dot(1132,365,6); dot(1190,365,6,(210,30,30)); arrow((1132,365),(1184,365)); dash((1040,365),(1190,365),fill=(18,102,204),w=2)
text(1115,330,'低点像',Fs); text(1167,330,'高点像',Fs)
d.rounded_rectangle((770,610,1300,698),radius=14,outline=(212,164,0),width=2,fill=(255,247,214))
text(792,628,'辐射中心：像底点 n',Fm)
text(792,660,'记法：地面“起伏”了 → 找 n',F)

# bottom
blue=(18,102,204)
d.rounded_rectangle((170,760,1230,865),radius=18,outline=blue,width=3,fill=(238,246,255))
text(700,785,'考试口诀：倾斜找 c，起伏找 n',Ftitle,blue,anchor='ma')
text(700,830,'像片倾斜位移看相机姿态；地形起伏位移看地面高差 h。',F,anchor='ma')

out='/home/ubuntu/resources/photogrammetry_tilt_relief_displacement.png'
img.save(out)
print(out)
print(Path(out).stat().st_size)
