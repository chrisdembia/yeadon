function stadiumsolid2

close all
axis equal off
hold on

%% define a lower stadium
s = struct;
s.t(1) = 2;
s.t(2) = 1.5;
s.r(1) = 1;
s.r(2) = .75;
s.h = 1;
s.angles = [0 pi/2 0];

c = [0 1 0];

% plots(s,1,c);
% plots(s,2,c);

view(30,60)

plotss2(s,c)

%% define an upper stadium

%% define distance bn stadia


end

function plots(s,i,c)

t = linspace(0,pi/2,5);

X = [s.t(i)+s.r(i)*cos(t)];
Y = [s.r(i)*sin(t)];

X = [X -X(end:-1:1) -X X(end:-1:1)];
Y = [Y Y(end:-1:1) -Y -Y(end:-1:1)];
Z = (i-1)*s.h*ones(1,length(X));

plot3([0 0],[0 0],[1 -1])
plot3([1 -1],[0 0],[0 0])
plot3([0 0],[1 -1],[0 0])
text(1,0,0,'x')
text(0,1,0,'y')
text(0,0,1,'z')
% 
% h = fill3(X,Y,Z,c,'EdgeColor',c);

POS = [X;Y;Z];
POS2 = R(s.angles)*POS;

X = POS2(1,:);
Y = POS2(2,:);
Z = POS2(3,:);

h = fill3(X,Y,Z,c,'EdgeColor','k');

alpha(h,.5)

end

function plotss2(s,c)

figure
hold on
axis off

t = linspace(0,pi/2,5);



X = [s.t(1)+s.r(1)*cos(t)];
X1 = [X -X(end:-1:1) -X X(end:-1:1)];
Y = [s.r(1)*sin(t)];
Y1 = [Y Y(end:-1:1) -Y -Y(end:-1:1)];
Z = zeros(1,length(t));
Z1 = [Z Z Z Z];

POS1 = [X1;Y1;Z1];

POS15 = R(s.angles)*POS1;

X1 = POS15(1,:);
Y1 = POS15(2,:);
Z1 = POS15(3,:);

X = [s.t(2)+s.r(2)*cos(t)];
X2 = [X -X(end:-1:1) -X X(end:-1:1)];
Y = [s.r(2)*sin(t)];
Y2 = [Y Y(end:-1:1) -Y -Y(end:-1:1)];
Z = s.h*ones(1,length(t));
Z2 = [Z Z Z Z];

POS2 = [X2;Y2;Z2];
POS25 = R(s.angles)*POS2;
X2 = POS25(1,:);
Y2 = POS25(2,:);
Z2 = POS25(3,:);

for i = 1:4*length(t)-1
    h = fill3([X1(i) X1(i+1) X2(i+1) X2(i)],[Y1(i) Y1(i+1) Y2(i+1) Y2(i)],[Z1(i) Z1(i+1) Z2(i+1) Z2(i)],c,'EdgeColor',c);
    alpha(h,.5)
end

plots(s,1,c);
plots(s,2,c);
axis equal
view(25,45)
end

function out = R(angles)

cx = cos(angles(1));
sx = sin(angles(1));

cy = cos(angles(2));
sy = sin(angles(2));

cz = cos(angles(3));
sz = sin(angles(3));

Rz = [cz -sz 0;
      sz  cz  0;
      0   0  1];
  
Ry = [cy  0  sy;
      0   1  0 ;
      -sy 0  cy];
  
Rx = [1   0 0;
      0   cx -sx;
      0   sx cx];
  
out = Rz * Ry * Rx;

end


























