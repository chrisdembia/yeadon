function stadiumsolid

close all
axis normal off
hold on

%% define a lower stadium
s = struct;
s.t(1) = 2;
s.t(2) = 1.5;
s.r(1) = 1;
s.r(2) = .75;
s.h = 1;
s.angle = [0 0 pi/3];

c = [0 1 0];

plots(s,1,c);
plots(s,2,c);

view(30,60)

plotss2(s,c)
% set alpha values =]

%% define an upper stadium

%% define distance bn stadia


end

function plots(s,i,c)

t = linspace(0,pi/2,5);
% X = [0 s.t(i)+s.r(i)*cos(t) 0 0];
% Y = [0 s.r(i)*sin(t) s.r(i) 0];

X = [s.t(i)+s.r(i)*cos(t)];
Y = [s.r(i)*sin(t)];

Z = (i-1)*s.h*ones(1,length(X));

POS = [X;Y;Z];

POS2 = 

X = POS2(1,:);
Y = POS2(2,:);
Z = POS2(3,:);

h = fill3([X -X(end:-1:1) -X X(end:-1:1)],[Y Y(end:-1:1) -Y -Y(end:-1:1)],[Z Z Z Z],c,'EdgeColor',c);

alpha(h,.5)

end

function plots2(s,i,c)

t = linspace(0,pi/2,5);
% X = [0 s.t(i)+s.r(i)*cos(t) 0 0];
% Y = [0 s.r(i)*sin(t) s.r(i) 0];

X = [s.t(i)+s.r(i)*cos(t)];
Y = [s.r(i)*sin(t)];

Z = (i-1)*s.h*ones(1,length(X));
h = fill3([X -X(end:-1:1) -X X(end:-1:1)],[Y Y(end:-1:1) -Y -Y(end:-1:1)],[Z Z Z Z],c,'EdgeColor','k');

alpha(h,.5)
end

function plotss2(s,c)

figure
hold on
axis off

t = linspace(0,pi/2,5);

Z = zeros(length(t));
Z1 = [Z Z Z Z];
Z = s.h*ones(length(t));
Z2 = [Z Z Z Z];

X = [s.t(1)+s.r(1)*cos(t)];
X1 = [X -X(end:-1:1) -X X(end:-1:1)];
X = [s.t(2)+s.r(2)*cos(t)];
X2 = [X -X(end:-1:1) -X X(end:-1:1)];
% X = [X1 X2];
% 
Y = [s.r(1)*sin(t)];
Y1 = [Y Y(end:-1:1) -Y -Y(end:-1:1)];
Y = [s.r(2)*sin(t)];
Y2 = [Y Y(end:-1:1) -Y -Y(end:-1:1)];
% Y = [Y1 Y2];
% 
% Z = [Z1 Z2];
% 
% size(X)
% size(Y)
% size(Z)
% h = surf(X,Y,Z,c,'EdgeColor',c);
% 
% alpha(h,.5)

plots2(s,1,c);
plots2(s,2,c);

for i = 1:4*length(t)-1
    h = fill3([X1(i) X1(i+1) X2(i+1) X2(i)],[Y1(i) Y1(i+1) Y2(i+1) Y2(i)],[0 0 s.h s.h],c,'EdgeColor',c);
    alpha(h,.5)
end

end

function plotss(s,c)

t = linspace(0,pi/2,5);
% X = [0 s.t(i)+s.r(i)*cos(t) 0 0];
% Y = [0 s.r(i)*sin(t) s.r(i) 0];

% X = [s.t(1)+s.r(1)*cos(t)];
% 
% Z = zeros(length(X));
% Z1 = [Z Z Z Z];
% Z = s.h*ones(length(X));
% Z2 = [Z Z Z Z];
% 
% X1 = [X -X(end:-1:1) -X X(end:-1:1)];
% X = [s.t(2)+s.r(2)*cos(t)];
% X2 = [X -X(end:-1:1) -X X(end:-1:1)];
% X = [X1 X2];
% 
% Y = [s.r(1)*sin(t)];
% Y1 = [Y Y(end:-1:1) -Y -Y(end:-1:1)];
% Y = [s.r(2)*sin(t)];
% Y2 = [Y Y(end:-1:1) -Y -Y(end:-1:1)];
% Y = [Y1 Y2];
% 
% Z = [Z1 Z2];
% 
% size(X)
% size(Y)
% size(Z)
% h = surf(X,Y,Z,c,'EdgeColor',c);
% 
% alpha(h,.5)


end

function out = R(angles)

cx = cos(angles(1));
sx = sin(angles(1));

cy = cos(angles(2));
sy = cos(angles(2));

cz = cos(angles(3));
sz = cos(angles(3));

Rx = [cx -sx 0;
      sx  0  0;
      0   0  1];
  
Ry = [cy  0  sy;
      0   1  0 ;
      -sy 0  cy];
  
Rz = [1   0 0;
      0   cz -sz;
      0   sz cz];
  
out = Rz * Ry * Rx;

end


























